SELECT
  year,
  month,
  day,
  COUNT(*) AS decision_events,
  AVG(
    TRY_CAST(json_extract_string(attributes, '$.pod_fill_rate') AS DOUBLE)
  ) AS avg_pod_fill_rate,
  AVG(
    TRY_CAST(json_extract_string(attributes, '$.pacing_allowed_count') AS DOUBLE)
  ) AS avg_pacing_allowed_count,
  AVG(
    TRY_CAST(json_extract_string(attributes, '$.ranked_candidate_count') AS DOUBLE)
  ) AS avg_ranked_candidate_count
FROM omniads_events
WHERE event_type = 'ad_decision_created'
GROUP BY year, month, day
ORDER BY year, month, day;