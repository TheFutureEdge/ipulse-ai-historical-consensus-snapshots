#!/usr/bin/env python3
"""Return whether a candidate contains data not already published as latest."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_LATEST_URL = (
    "https://huggingface.co/datasets/future-edge-group/"
    "ipulse-ai-historical-consensus-snapshots/resolve/main/data/latest.json"
)


def emit(name: str, value: str) -> None:
    print(f"{name}={value}")
    output = os.getenv("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as handle:
            handle.write(f"{name}={value}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--published-url", default=DEFAULT_LATEST_URL)
    args = parser.parse_args()

    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    try:
        with urllib.request.urlopen(args.published_url, timeout=30) as response:
            published = json.load(response)
    except urllib.error.HTTPError as exc:
        # The Hub can return either 401 or 404 before a public repository exists.
        # Both mean there is no readable public latest pointer to compare yet.
        if exc.code not in (401, 404):
            raise
        published = None

    changed = published is None or candidate["data_sha256"] != published.get("data_sha256")
    emit("material_update", str(changed).lower())
    emit("snapshot_id", candidate["snapshot_id"])


if __name__ == "__main__":
    main()
