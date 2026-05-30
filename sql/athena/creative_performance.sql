WITH creative_rollup AS (
  SELECT
    campaign_id,
    creative_id,
    COUNT(CASE WHEN event_type = 'impression_received' THEN 1 END) AS impressions,
    COUNT(CASE WHEN event_type = 'click_received' THEN 1 END) AS clicks,
    COUNT(CASE WHEN event_type = 'conversion_received' THEN 1 END) AS conversions
  FROM omniads_analytics.omniads_events
  WHERE year = '2026'
    AND month = '05'
    AND day = '30'
    AND campaign_id IS NOT NULL
    AND creative_id IS NOT NULL
  GROUP BY campaign_id, creative_id
)

SELECT
  campaign_id,
  creative_id,
  impressions,
  clicks,
  conversions,
  CASE
    WHEN impressions = 0 THEN 0
    ELSE ROUND(clicks * 1.0 / impressions, 4)
  END AS ctr,
  CASE
    WHEN clicks = 0 THEN 0
    ELSE ROUND(conversions * 1.0 / clicks, 4)
  END AS cvr
FROM creative_rollup
ORDER BY impressions DESC, clicks DESC;