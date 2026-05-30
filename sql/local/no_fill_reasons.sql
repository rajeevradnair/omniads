SELECT
  COALESCE(
    json_extract_string(attributes, '$.no_fill_reason'),
    status,
    'UNKNOWN'
  ) AS no_fill_reason,
  COUNT(*) AS no_fill_count
FROM omniads_events
WHERE event_type = 'no_fill_returned'
GROUP BY no_fill_reason
ORDER BY no_fill_count DESC;