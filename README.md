---
license: cc-by-4.0
language:
- en
pretty_name: iPulse AI Historical Consensus Snapshots
tags:
- finance
- forecasting
- agentic-ai
- market-research
- reproducibility
configs:
- config_name: snapshots
  data_files:
  - split: train
    path: data/snapshots/*.parquet
---

# iPulse AI Historical Consensus Snapshots

This dataset contains immutable, historical consensus outputs produced by iPulse AI, Future Edge Group's Open Agentic Investment Research Platform. It is intended to make selected research outputs inspectable without disclosing raw prompts, individual advisor responses, proprietary price paths, licensed market-data payloads, or internal infrastructure.

The first snapshot contains 746 asset-horizon records for 373 assets across 1-year and 5-year horizons. The batch generation date is 2026-07-05 and the canonical scoring run completed on 2026-07-08.

## Important interpretation

These are model-generated forecasts, not observed results. This release does not measure accuracy, benchmark performance, calibration, profitability, or investment outcomes. Evaluation is a separate future workstream.

Nothing here is personal investment advice, a current recommendation, or an instruction to buy or sell. The numeric iPulse consensus score and supporting metrics are historical research outputs. BUY/SELL-style signal bands are intentionally excluded from schema 1.0.0.

## Version mapping

The version fields describe different layers and are not expected to match:

| Field | Batch 6 value | Meaning |
|---|---|---|
| `source_algorithm_version` | `v2.5` | Exact production run version stored with the source rows. |
| `public_methodology_version` | `v7.4` | Public scoring-methodology family represented by the run. |
| `evaluation_methodology_version` | `not_applicable_not_evaluated` | No accuracy or performance evaluation is included. |
| `dataset_schema_version` | `1.0.0` | Public dataset column contract. |

The more specific `scoring_architecture_version` for this snapshot is `v7.4_confidence_adjusted_excess_return_event_risk`.

## Coverage and cohort rule

The earlier generated Batch 6 population contained 377 assets. The canonical production scoring cohort contains 373. Four assets were intentionally excluded because their forecast anchors were outside the production five-day anchor window ending 2026-07-05:

- Brent Crude Spot in US Dollar — anchor 2026-06-15
- Palladium Spot in US Dollar — anchor 2026-06-26
- Platinum Spot in US Dollar — anchor 2026-06-26
- Victoria's Secret & Co — anchor 2026-06-26

This is a cohort-freshness exclusion, not an accuracy or performance decision.

## Contents

- `data/snapshots/`: immutable Parquet snapshots
- `data/latest.json`: machine-readable pointer and data checksum
- `schema/`: JSON schema and field dictionary
- `methodology/`: methodology and interpretation notes
- `metadata/`: provenance and checksum manifest
- `reports/`: release-specific data-quality reports
- `scripts/`: exact export and validation logic

## Known limitations

- The snapshot is heavily weighted toward equities: 347 of 373 assets.
- The asset set is a production cohort, not a statistically representative market sample.
- Only consensus-level processed outputs are included; users cannot reconstruct individual advisor forecasts from this dataset.
- Expected-return figures are forecasts and may be negative, extreme, inconsistent, or wrong.
- Financial-health scores are not applicable or unavailable for some asset classes; the accompanying status field explains those nulls.
- Historical publication does not remove model risk, selection bias, or the possibility of data and software defects.

## Reproducibility and integrity

The exact BigQuery sources, filters, SQL, field allowlist, row-level checksums, and Parquet checksum are included. The transformation can reproduce the public snapshot for an authorized operator with read access to the governed source tables. It does not grant access to or redistribute the excluded source payloads.

See [the methodology](methodology/consensus-snapshot-methodology.md), [data dictionary](schema/data-dictionary.md), and [quality report](reports/quality-report-2026-07-05.md).

## License and citation

The public dataset package is licensed under CC BY 4.0. Attribution should identify **iPulse AI** and **Future Edge Group FZE** and include the immutable `snapshot_id` and data checksum.

Suggested citation:

> Future Edge Group FZE. “iPulse AI Historical Consensus Snapshots.” Batch 6 snapshot dated 2026-07-05, dataset schema 1.0.0.

## Contact

Product: **iPulse AI**  
Organization: **Future Edge Group FZE**  
Founder: **Russlan Ramdowar**
