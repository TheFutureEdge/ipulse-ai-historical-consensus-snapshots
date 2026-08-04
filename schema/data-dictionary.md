# Data dictionary — schema 1.0.0

The dataset grain is one sealed snapshot × public-safe asset × forecast horizon.

| Field | Type | Meaning |
|---|---|---|
| `record_id` | string | Deterministic SHA-256 public record identifier. |
| `snapshot_id` | string | Immutable release identifier. |
| `batch_id` | integer | Internal production batch number, safe at aggregate level. |
| `batch_generation_date` | date | Date used to identify the canonical batch cohort. |
| `forecast_anchor_start_date` | date | Earliest anchor date among inputs to the consensus row. |
| `forecast_anchor_end_date` | date | Latest anchor date among inputs to the consensus row. |
| `scoring_completed_at_utc` | timestamp | Time the canonical consensus row was scored. |
| `asset_symbol` | string | iPulse AI public asset symbol. |
| `asset_name` | string | Public display name. |
| `asset_category` | string | Broad asset class. |
| `asset_category_detailed` | string/null | More detailed class where available. |
| `contract_or_ownership_type` | string/null | Instrument or ownership classification. |
| `ticker` | string/null | Exchange ticker where applicable. |
| `exchange_code` | string/null | Public exchange code where applicable. |
| `currency` | string/null | Quotation currency where applicable. |
| `forecast_horizon` | string | `1y` or `5y`. |
| `ipulse_consensus_score` | integer | Signed historical consensus score; not a probability or realized return. |
| `annualized_expected_return_pct` | number | Forecast annualized expected total return percentage. |
| `forecast_return_mad_pct` | number | Median absolute deviation of forecast returns, in percentage points. |
| `direction_consistency` | number | Direction consistency measure. |
| `direction_agreement` | number | Cross-voice direction agreement measure. |
| `risk_pressure_score` | number | Event-risk pressure measure. |
| `risk_resilience_score` | number | Risk-resilience measure. |
| `financial_health_score` | number/null | Financial-health measure when applicable and supported. |
| `financial_health_status` | string | Availability/applicability status for financial health. |
| `voice_count` | integer | Number of contributing voices. |
| `advisor_count` | integer | Number of contributing advisor identities after aggregation. |
| `persona_count` | integer | Number of represented research personas. |
| `model_count` | integer | Number of represented model families. |
| `source_algorithm_version` | string | Exact stored production run version. |
| `public_methodology_version` | string | Public scoring-methodology family version. |
| `evaluation_methodology_version` | string | Explicit evaluation version; not applicable in this release. |
| `dataset_schema_version` | string | Public column-contract version. |
| `scoring_architecture_version` | string | Detailed scoring architecture recorded by production. |
| `risk_resilience_formula_version` | string | Risk-resilience formula identifier. |
| `financial_health_formula_version` | string/null | Financial-health formula identifier where applicable. |
| `methodology_url` | string | Canonical methodology file for this dataset. |
| `record_checksum` | string | SHA-256 of the row's public field values. |
