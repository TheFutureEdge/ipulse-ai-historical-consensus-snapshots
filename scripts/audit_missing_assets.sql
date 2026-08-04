WITH generated_v23 AS (
  SELECT DISTINCT subject_id
  FROM `data-platform-436809.prod__dp_oracle_fincore_prediction_market__analytics.prediction_consensus_scoring`
  WHERE scoring_batch = 6
    AND score_snapshot_kind = 'ORIGINAL'
    AND recompute_date = DATE '2026-07-05'
    AND scoring_algorithm_version = 'v2.3'
),
canonical_v25 AS (
  SELECT DISTINCT subject_id
  FROM `data-platform-436809.prod__dp_oracle_fincore_prediction_market__analytics.prediction_consensus_scoring`
  WHERE scoring_batch = 6
    AND score_snapshot_kind = 'ORIGINAL'
    AND recompute_date = DATE '2026-07-05'
    AND scoring_algorithm_version = 'v2.5'
),
missing AS (
  SELECT subject_id
  FROM generated_v23
  LEFT JOIN canonical_v25 USING (subject_id)
  WHERE canonical_v25.subject_id IS NULL
)
SELECT
  assets.name AS asset_name,
  assets.subject_category AS asset_category,
  MIN(DATE(status.forecast_horizon_anchor_value_timestamp_utc)) AS anchor_start_date,
  MAX(DATE(status.forecast_horizon_anchor_value_timestamp_utc)) AS anchor_end_date,
  COUNT(*) AS source_voice_rows
FROM missing
JOIN `data-platform-436809.prod__dp_oracle_fincore__controls.dim_fincore_market_assets` AS assets
  ON missing.subject_id = assets.asset_id
JOIN `data-platform-436809.prod__dp_oracle_fincore_prediction_market__datasets.prediction_status` AS status
  ON missing.subject_id = status.subject_id
  AND status.scoring_batch = 6
GROUP BY asset_name, asset_category
ORDER BY asset_name
