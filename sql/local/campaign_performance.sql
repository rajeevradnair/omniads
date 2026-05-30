WITH event_rollup AS (
  SELECT
    campaign_id,
    COUNT(*) FILTER (WHERE event_type = 'impression_received') AS impressions,
    COUNT(*) FILTER (WHERE event_type = 'click_received') AS clicks,
    COUNT(*) FILTER (WHERE event_type = 'conversion_received') AS conversions
  FROM omniads_events
  WHERE campaign_id IS NOT NULL
  GROUP BY campaign_id
)

SELECT
  campaign_id,
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
FROM event_rollup
ORDER BY impressions DESC, clicks DESC;