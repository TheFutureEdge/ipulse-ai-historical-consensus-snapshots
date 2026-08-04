# Consensus snapshot methodology

Version: v7.4  
Dataset schema: 1.0.0

## What is published

Each row is one historical iPulse AI consensus result for one public-safe asset identifier and one forecast horizon in one sealed production snapshot. Batch 6 has exactly two rows per asset: one for `1y` and one for `5y`.

The release contains the consensus score, expected-return estimate, dispersion, direction-consistency and direction-agreement measures, selected risk and financial-health measures, contributor counts, and explicit version metadata.

## What is not published

The release excludes raw model requests and responses, prompts, individual advisor outputs, thesis text, generated price paths, provider market-data payloads, current recomputations, internal identifiers, storage locations, credentials, and BUY/SELL-style signal bands.

## Metric interpretation

- `ipulse_consensus_score`: signed production consensus score. Higher and lower values reflect the scoring architecture's combined forecast and risk evidence; it is not a probability, realized return, or performance statistic.
- `annualized_expected_return_pct`: consensus annualized expected total return, in percentage points, including dividends where applicable.
- `forecast_return_mad_pct`: median absolute deviation of the annualized return forecasts, in percentage points; larger values indicate greater cross-forecast dispersion.
- `direction_consistency`: consistency of forecast direction across the underlying horizon path.
- `direction_agreement`: agreement in forecast direction among the contributing voices.
- `risk_pressure_score`: event-risk pressure measure used by the scoring architecture.
- `risk_resilience_score`: risk-resilience measure derived under the named formula version.
- `financial_health_score`: asset financial-health measure when applicable and sufficiently supported. Interpret it together with `financial_health_status`.
- contributor counts: numbers of voices, advisors, personas, and model families represented in the stored consensus inputs. They do not identify contributors.

## Cohort construction

The canonical source is the production `ORIGINAL` snapshot for Batch 6, recompute date 2026-07-05, run version v2.5, `non_adjusted` voice-count mode, and horizons `1y` and `5y`.

Production kept forecast anchors from 2026-06-30 through 2026-07-05, a five-day lag window ending on the final batch generation date. Four otherwise generated assets had stale anchors before this interval and were excluded. The published population is therefore 373 assets and 746 asset-horizon rows.

## Version layers

- Source algorithm v2.5 identifies the exact stored production run.
- Public methodology v7.4 identifies the public formula family.
- Architecture `v7.4_confidence_adjusted_excess_return_event_risk` identifies the detailed scoring configuration recorded in the source parameters.
- Evaluation methodology is not applicable because this dataset contains no outcome evaluation.
- Dataset schema 1.0.0 identifies the public column contract.

## Publication policy

A snapshot becomes eligible when it is a sealed canonical `ORIGINAL` batch, is no longer a live/current research output, passes the allowlist and quality checks, and is explicitly approved for release. There is no fixed 30-day accuracy wait. Accuracy is not assessed in this workflow.

Re-exporting identical data is a no-op. Corrections must use a new immutable revision with a documented reason and must preserve prior public history.
