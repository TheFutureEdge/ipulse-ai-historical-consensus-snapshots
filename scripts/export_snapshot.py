#!/usr/bin/env python3
"""Export one immutable, public-safe iPulse AI consensus snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from google.cloud import bigquery


REPO_ID = "future-edge-group/ipulse-ai-historical-consensus-snapshots"
METHODOLOGY_URL = (
    "https://huggingface.co/datasets/"
    f"{REPO_ID}/blob/main/methodology/consensus-snapshot-methodology.md"
)


def scalar(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def row_checksum(row: pd.Series) -> str:
    payload = {column: scalar(row[column]) for column in row.index if column != "record_checksum"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--project", default="data-platform-436809")
    parser.add_argument("--batch-id", type=int, default=6)
    parser.add_argument("--snapshot-date", type=date.fromisoformat, default=date(2026, 7, 5))
    parser.add_argument("--source-algorithm-version", default="v2.5")
    args = parser.parse_args()

    root = args.output_root.resolve()
    sql = (Path(__file__).with_suffix(".sql")).read_text(encoding="utf-8")
    snapshot_id = (
        f"ipulse-consensus-batch{args.batch_id}-"
        f"{args.snapshot_date.isoformat()}-{args.source_algorithm_version}"
    )
    parameters = [
        bigquery.ScalarQueryParameter("batch_id", "INT64", args.batch_id),
        bigquery.ScalarQueryParameter("snapshot_date", "DATE", args.snapshot_date),
        bigquery.ScalarQueryParameter(
            "source_algorithm_version", "STRING", args.source_algorithm_version
        ),
        bigquery.ScalarQueryParameter("snapshot_id", "STRING", snapshot_id),
        bigquery.ScalarQueryParameter("methodology_url", "STRING", METHODOLOGY_URL),
    ]
    frame = bigquery.Client(project=args.project).query(
        sql, job_config=bigquery.QueryJobConfig(query_parameters=parameters)
    ).to_dataframe()

    # Remove BigQuery-specific extension dtypes so the Parquet file is portable
    # outside the export environment and renders cleanly in the Hub viewer.
    for column in (
        "batch_generation_date",
        "forecast_anchor_start_date",
        "forecast_anchor_end_date",
    ):
        frame[column] = frame[column].map(lambda value: value.isoformat()).astype("string")
    frame["scoring_completed_at_utc"] = pd.to_datetime(
        frame["scoring_completed_at_utc"], utc=True
    )

    frame.insert(
        0,
        "record_id",
        frame.apply(
            lambda row: hashlib.sha256(
                (
                    f"{row['snapshot_id']}|{row['asset_category']}|"
                    f"{row['asset_symbol']}|{row['forecast_horizon']}"
                ).encode("utf-8")
            ).hexdigest(),
            axis=1,
        ),
    )
    frame["record_checksum"] = frame.apply(row_checksum, axis=1)
    frame = frame.sort_values(
        ["asset_category", "asset_symbol", "forecast_horizon"], kind="stable"
    ).reset_index(drop=True)

    snapshot_path = root / "data" / "snapshots" / f"{args.snapshot_date.isoformat()}.parquet"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(snapshot_path, index=False, compression="zstd")

    latest = {
        "snapshot_id": snapshot_id,
        "snapshot_date": args.snapshot_date.isoformat(),
        "batch_id": args.batch_id,
        "row_count": int(len(frame)),
        "asset_count": int(frame["asset_symbol"].nunique()),
        "horizons": sorted(frame["forecast_horizon"].unique().tolist()),
        "source_algorithm_version": args.source_algorithm_version,
        "public_methodology_version": "v7.4",
        "evaluation_methodology_version": "not_applicable_not_evaluated",
        "dataset_schema_version": "1.0.0",
        "data_path": str(snapshot_path.relative_to(root)),
        "data_sha256": file_sha256(snapshot_path),
    }
    (root / "data" / "latest.json").write_text(
        json.dumps(latest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(latest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
