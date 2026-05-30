SELECT
  COALESCE(
    json_extract_scalar(attributes, '$.no_fill_reason'),
    status,
    'UNKNOWN'
  ) AS no_fill_reason,
  COUNT(*) AS no_fill_count
FROM omniads_analytics.omniads_events
WHERE year = '2026'
  AND month = '05'
  AND day = '30'
  AND event_type = 'no_fill_returned'
GROUP BY
  COALESCE(
    json_extract_scalar(attributes, '$.no_fill_reason'),
    status,
    'UNKNOWN'
  )
ORDER BY no_fill_count DESC;