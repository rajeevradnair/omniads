WITH event_counts AS (
  SELECT
    year,
    month,
    day,
    COUNT(CASE WHEN event_type = 'ad_decision_created' THEN 1 END) AS ad_decisions,
    COUNT(CASE WHEN event_type = 'vast_returned' THEN 1 END) AS vast_returns,
    COUNT(CASE WHEN event_type = 'no_fill_returned' THEN 1 END) AS no_fills
  FROM omniads_analytics.omniads_events
  WHERE year = '2026'
    AND month = '05'
    AND day = '30'
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
FROM event_counts;