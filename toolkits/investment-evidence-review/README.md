# Investment evidence review toolkit

Russlan Ramdowar, Future Edge Group. Version 1.0, 5 October 2026.

These five empty CSV worksheets help reviewers keep evidence, definitions,
assumptions and invalidation tests separate. They contain no security
recommendation, portfolio holdings, client data or fabricated example values.

## Start with an auditable archive

Run [Are Archived Forecasts Ready for Evaluation?](../../notebooks/02_forecast_evaluation_readiness.ipynb),
also [published and executed on Kaggle](https://www.kaggle.com/code/russlan/are-archived-forecasts-ready-for-evaluation).
It verifies the immutable 746-record Batch 6 input by SHA-256, checks complete
horizon pairs, measures maturity at a fixed date and distinguishes recorded
timestamps from a source-information cutoff. All records remain unevaluated;
the notebook does not report a forecasting track record.

## Use the worksheets

| Worksheet | What to record | Review gate |
|---|---|---|
| evidence-register.csv | Primary source URL, original field/excerpt, reporting period, publication time, retrieval time, decision cutoff and checksum | A later retrieval does not prove the source existed before the decision; preserve its original publication/version evidence. |
| cash-flow-reconciliation.csv | As-reported net income, operating cash flow and capex with currency, units, period and sign convention | Match periods and units before arithmetic; explain adjustments instead of silently changing signs. |
| valuation-assumptions.csv | Each scenario input, formula, units, source, uncertainty and sensitivity | Separate reported facts from assumptions. A chosen valuation input is not a measured outcome. |
| thesis-invalidation.csv | Supporting and contradicting evidence and a measurable condition that would change the thesis | Record a test before the outcome; preserve revisions and their reasons. |
| forecast-outcome-review.csv | Original forecast, horizon, information cutoff, outcome source, corporate actions, FX, benchmark and evaluation version | Mark immature or missing observations explicitly; never replace them with zero returns. |

The files deliberately contain headers only. Add one row per named record;
blank means unavailable, not zero or passed. Keep evidence IDs stable across
the sheets. Use ISO dates and UTC timestamps, preserving the source timezone
when a conversion matters. Record unknown cutoff timestamps as unknown.

For cash-flow work, preserve the issuer's exact line labels and accounting
framework. If defining a CFO-minus-capex measure, document capex as a positive
cash outflow and compute operating cash flow minus that outflow. This is a
chosen research definition; it does not capture every reinvestment requirement
or establish valuation. Keep acquisitions, leases and other adjustments
visible. Use annual with annual and quarter with quarter; do not compare a
year-to-date flow with one isolated quarter. Do not apply a percentage growth
formula blindly across zero or sign-changing bases.

The [SEC financial-statement guide](https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide)
explains the distinction between income and cash flow and the operating,
investing and financing sections. Actual company figures must come from the
relevant primary filing and footnotes. No company-specific accounting claim is
made by these blank worksheets.

## Reproduce the companion notebook

From the repository root:

```sh
python -m pip install -r requirements-notebooks.txt
jupyter nbconvert --execute --to notebook --output /tmp/readiness-executed.ipynb notebooks/02_forecast_evaluation_readiness.ipynb
```

The notebook downloads one public pinned Parquet input when its local cache is
absent, verifies SHA-256 and saves a JSON audit plus two figures. It requires
no credentials. Its audit date is fixed at 2026-10-05. The six-field archive
audit and the separate 766-record equity return-aggregation study are distinct
populations; never merge their counts.

## Author, source and licence

Future Edge Group develops [iPulse AI](https://ipulseai.com), an Open Agentic
Investment Research Platform, and [Forecast Library](https://forecastlibrary.com).
Affiliation is disclosed because this companion uses a first-party public
dataset. Related evidence: [the six-field audit](https://dev.to/futureedgegroup/audit-your-ai-forecast-dataset-before-calling-it-a-benchmark-29f)
and [return-aggregation research](https://ipulseai.com/concepts/how-to-compare-ai-stock-forecasts-cagr-and-total-return).

Dataset, worksheets and documentation: CC BY 4.0, as in the repository licence.
New notebook code: Apache 2.0; the embedded dataset results retain CC BY 4.0
attribution. The notebook does not change the underlying dataset licence.
