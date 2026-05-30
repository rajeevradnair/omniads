WITH event_counts AS (
  SELECT
    year,
    month,
    day,
    COUNT(*) FILTER (WHERE event_type = 'ad_decision_created') AS ad_decisions,
    COUNT(*) FILTER (WHERE event_type = 'vast_returned') AS vast_returns,
    COUNT(*) FILTER (WHERE event_type = 'no_fill_returned') AS no_fills
  FROM omniads_events
  GROUP BY year, month, day
)

SELECT
  year,
  month,
  day,
  ad_decisions,
  vast_returns,
  no_fills,
  CASE
    WHEN ad_decisions = 0 THEN 0
    ELSE ROUND(vast_returns * 1.0 / ad_decisions, 4)
  END AS fill_rate,
  CASE
    WHEN ad_decisions = 0 THEN 0
    ELSE ROUND(no_fills * 1.0 / ad_decisions, 4)
  END AS no_fill_rate
FROM event_counts
ORDER BY year, month, day;