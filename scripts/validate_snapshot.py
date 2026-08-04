#!/usr/bin/env python3
"""Fail closed when a snapshot violates the approved public schema or invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "record_id", "snapshot_id", "batch_id", "batch_generation_date",
    "forecast_anchor_start_date", "forecast_anchor_end_date",
    "scoring_completed_at_utc", "asset_symbol", "asset_name", "asset_category",
    "asset_category_detailed", "contract_or_ownership_type", "ticker",
    "exchange_code", "currency", "forecast_horizon", "ipulse_consensus_score",
    "annualized_expected_return_pct", "forecast_return_mad_pct",
    "direction_consistency", "direction_agreement", "risk_pressure_score",
    "risk_resilience_score", "financial_health_score", "financial_health_status",
    "voice_count", "advisor_count", "persona_count", "model_count",
    "source_algorithm_version", "public_methodology_version",
    "evaluation_methodology_version", "dataset_schema_version",
    "scoring_architecture_version", "risk_resilience_formula_version",
    "financial_health_formula_version", "methodology_url", "record_checksum",
]
FORBIDDEN_COLUMN_PARTS = (
    "subject_id", "task_id", "request", "response", "prompt", "thesis",
    "price_path", "storage", "bucket", "raw_extract", "signal",
)
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-rows", type=int)
    parser.add_argument("--expected-assets", type=int)
    args = parser.parse_args()

    root = args.root.resolve()
    latest = json.loads((root / "data" / "latest.json").read_text(encoding="utf-8"))
    path = root / latest["data_path"]
    frame = pd.read_parquet(path)
    errors: list[str] = []

    if list(frame.columns) != REQUIRED_COLUMNS:
        errors.append("column order or allowlist does not match schema 1.0.0")
    forbidden = [c for c in frame.columns if any(part in c.lower() for part in FORBIDDEN_COLUMN_PARTS)]
    if forbidden:
        errors.append(f"forbidden columns present: {forbidden}")
    if args.expected_rows is not None and len(frame) != args.expected_rows:
        errors.append(f"expected {args.expected_rows} rows, found {len(frame)}")
    if args.expected_assets is not None and frame["asset_symbol"].nunique() != args.expected_assets:
        errors.append(f"expected {args.expected_assets} assets")
    if len(frame) != 2 * frame["asset_symbol"].nunique():
        errors.append("expected exactly two horizon rows per asset")
    if frame["record_id"].nunique() != len(frame):
        errors.append("record_id is not unique")
    if frame.duplicated(["snapshot_id", "asset_category", "asset_symbol", "forecast_horizon"]).any():
        errors.append("duplicate snapshot/asset/horizon keys")
    if set(frame["forecast_horizon"]) != {"1y", "5y"}:
        errors.append("forecast horizons must be exactly 1y and 5y")
    if frame[["record_id", "asset_symbol", "asset_name", "asset_category", "ipulse_consensus_score"]].isna().any().any():
        errors.append("required identity or score values contain nulls")
    if set(frame["source_algorithm_version"]) != {"v2.5"}:
        errors.append("unexpected source algorithm version")
    if set(frame["public_methodology_version"]) != {"v7.4"}:
        errors.append("unexpected public methodology version")
    if set(frame["evaluation_methodology_version"]) != {"not_applicable_not_evaluated"}:
        errors.append("this dataset must remain explicitly unevaluated")
    if set(frame["dataset_schema_version"]) != {"1.0.0"}:
        errors.append("unexpected dataset schema version")
    if file_sha256(path) != latest["data_sha256"]:
        errors.append("Parquet checksum differs from data/latest.json")

    text = "\n".join(
        frame.select_dtypes(include=["object", "string"]).fillna("").astype(str).stack().tolist()
    )
    if UUID.search(text):
        errors.append("UUID-shaped internal identifier found in public values")

    result = {
        "status": "failed" if errors else "passed",
        "errors": errors,
        "row_count": len(frame),
        "asset_count": int(frame["asset_symbol"].nunique()),
        "horizons": sorted(frame["forecast_horizon"].unique().tolist()),
        "score_min": int(frame["ipulse_consensus_score"].min()),
        "score_max": int(frame["ipulse_consensus_score"].max()),
        "null_financial_health_scores": int(frame["financial_health_score"].isna().sum()),
        "data_sha256": latest["data_sha256"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
