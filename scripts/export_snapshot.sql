WITH canonical_scoring AS (
  SELECT *
  FROM `data-platform-436809.prod__dp_oracle_fincore_prediction_market__analytics.prediction_consensus_scoring`
  WHERE scoring_batch = @batch_id
    AND score_snapshot_kind = 'ORIGINAL'
    AND recompute_date = @snapshot_date
    AND scoring_algorithm_version = @source_algorithm_version
    AND voices_count_mode = 'non_adjusted'
    AND horizon_config IN ('1y', '5y')
),
anchor_dates AS (
  SELECT
    scoring.scoring_result_id,
    MIN(DATE(status.forecast_horizon_anchor_value_timestamp_utc)) AS forecast_anchor_start_date,
    MAX(DATE(status.forecast_horizon_anchor_value_timestamp_utc)) AS forecast_anchor_end_date
  FROM canonical_scoring AS scoring
  CROSS JOIN UNNEST(JSON_VALUE_ARRAY(scoring.scoring_input_task_ids)) AS task_id
  JOIN `data-platform-436809.prod__dp_oracle_fincore_prediction_market__datasets.prediction_status` AS status
    ON status.prediction_request_task_id = task_id
  GROUP BY scoring.scoring_result_id
)
SELECT
  @snapshot_id AS snapshot_id,
  scoring.scoring_batch AS batch_id,
  scoring.recompute_date AS batch_generation_date,
  anchors.forecast_anchor_start_date,
  anchors.forecast_anchor_end_date,
  scoring.scored_at_utc AS scoring_completed_at_utc,
  assets.asset_symbol_pulse AS asset_symbol,
  COALESCE(assets.name, scoring.subject_name) AS asset_name,
  LOWER(COALESCE(assets.subject_category, scoring.subject_category)) AS asset_category,
  assets.subject_category_detailed AS asset_category_detailed,
  assets.contract_or_ownership_type,
  assets.ticker_on_exchange AS ticker,
  assets.exchange_code_pulse AS exchange_code,
  assets.currency,
  scoring.horizon_config AS forecast_horizon,
  scoring.consensus_score_incl_divds AS ipulse_consensus_score,
  scoring.annual_mean_return_pct_incl_divds AS annualized_expected_return_pct,
  scoring.annual_return_mad_pct_incl_divds AS forecast_return_mad_pct,
  scoring.direction_consistency,
  scoring.dir_agree AS direction_agreement,
  scoring.risk_pressure_score,
  scoring.risk_resilience_score,
  scoring.financial_health_score,
  scoring.financial_health_status,
  CAST(JSON_VALUE(scoring.voice_counts, '$.n_voices') AS INT64) AS voice_count,
  CAST(JSON_VALUE(scoring.voice_counts, '$.n_analysts') AS INT64) AS advisor_count,
  CAST(JSON_VALUE(scoring.voice_counts, '$.n_personas') AS INT64) AS persona_count,
  CAST(JSON_VALUE(scoring.voice_counts, '$.n_models') AS INT64) AS model_count,
  scoring.scoring_algorithm_version AS source_algorithm_version,
  'v7.4' AS public_methodology_version,
  'not_applicable_not_evaluated' AS evaluation_methodology_version,
  '1.0.0' AS dataset_schema_version,
  JSON_VALUE(scoring.scoring_parameters, '$.scoring_architecture') AS scoring_architecture_version,
  scoring.risk_resilience_formula_version,
  scoring.financial_health_formula_version,
  @methodology_url AS methodology_url
FROM canonical_scoring AS scoring
JOIN anchor_dates AS anchors
  USING (scoring_result_id)
JOIN `data-platform-436809.prod__dp_oracle_fincore__controls.dim_fincore_market_assets` AS assets
  ON scoring.subject_id = assets.asset_id
ORDER BY asset_category, asset_symbol, forecast_horizon
