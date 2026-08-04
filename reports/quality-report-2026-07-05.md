# Data-quality report — Batch 6 snapshot

Status: **PASSED — suitable for owner approval and public upload**  
Snapshot: `ipulse-consensus-batch6-2026-07-05-v2.5`  
Schema: `1.0.0`

## Decision

The candidate is trustworthy for its stated purpose: publishing a historical consensus-output snapshot. It is not evidence of forecast accuracy or investment performance.

## Profile

| Check | Result |
|---|---:|
| Rows | 746 |
| Distinct assets | 373 |
| Distinct asset-horizon keys | 746 |
| Horizons | 1y, 5y |
| Asset mix | 347 equity; 14 crypto; 5 forex; 5 index; 2 commodity |
| iPulse score range | -703 to 492 |
| Annualized expected-return range | -49.1% to 54.5% |
| Forecast-return MAD range | 0.86 to 48.1 percentage points |
| Voice counts | 11 or 12 |
| Missing required identity, score, risk, or directional metrics | 0 |
| Null financial-health scores | 56, explained by status |
| Data checksum | `7361482200e068969ae539ae78794441f62cc32c047494dda6ffb7aaed3db9e9` |

Financial-health statuses are 660 `AVAILABLE`, 52 `NOT_APPLICABLE`, 30 `PARTIAL`, and 4 `INSUFFICIENT_DATA` rows. Null scores are allowed only because this field is not applicable or sufficiently supported for every asset.

## Grain and uniqueness

The intended grain is one sealed snapshot × public-safe asset × forecast horizon. All 746 keys and all deterministic `record_id` values are unique. Every asset has both required horizons.

## Version check

Every row maps the layers explicitly:

- source algorithm: `v2.5`
- public methodology: `v7.4`
- scoring architecture: `v7.4_confidence_adjusted_excess_return_event_risk`
- evaluation methodology: `not_applicable_not_evaluated`
- dataset schema: `1.0.0`

This confirms that the v2.5/v7.4 difference is intentional rather than a data conflict.

## Four-asset discrepancy

The generated v2.3 population had 377 assets; the canonical v2.5 population has 373. The production pipeline applies a five-day anchor window from 2026-06-30 through 2026-07-05. Four assets were outside it: Brent Crude (2026-06-15), Palladium (2026-06-26), Platinum (2026-06-26), and Victoria's Secret & Co (2026-06-26).

The exact comparison is in `scripts/audit_missing_assets.sql`. The production implementation describes the filter as protection against stale anchors. This is a documented cohort rule, not unresolved data loss.

## Safety and scope checks

Validation fails if the export contains internal IDs, task/request/response fields, prompt or thesis fields, storage fields, price paths, signal bands, duplicate keys, an unexpected horizon, an unexpected version, or a UUID-shaped public value.

The candidate contains none of those prohibited fields. Asset identifiers come only from the public-safe dimension allowlist. The export does not query raw prompt/response columns or provider market-data payloads.

## Remaining limitation

The check establishes structural correctness and source fidelity for the published snapshot. It does not test model accuracy, realized returns, calibration, benchmark outperformance, or investment suitability.
