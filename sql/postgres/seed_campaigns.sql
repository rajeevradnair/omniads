INSERT INTO advertisers (advertiser_id, advertiser_name, industry)
VALUES
    ('adv_streamfuel', 'StreamFuel Sports Drink', 'Consumer Beverage'),
    ('adv_quickcart', 'QuickCart Grocery Delivery', 'Retail Grocery'),
    ('adv_autosure', 'AutoSure Car Insurance', 'Insurance'),
    ('adv_fitpulse', 'FitPulse Smartwatch', 'Consumer Electronics')
ON CONFLICT (advertiser_id) DO NOTHING;

INSERT INTO campaigns (
    campaign_id,
    advertiser_id,
    campaign_name,
    objective,
    status,
    daily_budget_usd,
    base_bid_cpm_usd,
    starts_at,
    ends_at
)
VALUES
    (
        'camp_streamfuel_live_sports',
        'adv_streamfuel',
        'StreamFuel Live Sports Awareness',
        'AWARENESS',
        'ACTIVE',
        5000.00,
        12.5000,
        NOW() - INTERVAL '1 day',
        NOW() + INTERVAL '30 days'
    ),
    (
        'camp_quickcart_match_day',
        'adv_quickcart',
        'QuickCart Match Day Delivery',
        'CONVERSION',
        'ACTIVE',
        3500.00,
        10.0000,
        NOW() - INTERVAL '1 day',
        NOW() + INTERVAL '30 days'
    ),
    (
        'camp_autosure_sports_fans',
        'adv_autosure',
        'AutoSure Sports Fans Protection',
        'LEAD_GENERATION',
        'ACTIVE',
        4200.00,
        9.7500,
        NOW() - INTERVAL '1 day',
        NOW() + INTERVAL '30 days'
    ),
    (
        'camp_fitpulse_performance',
        'adv_fitpulse',
        'FitPulse Performance Watch',
        'CONSIDERATION',
        'ACTIVE',
        6000.00,
        14.2500,
        NOW() - INTERVAL '1 day',
        NOW() + INTERVAL '30 days'
    )
ON CONFLICT (campaign_id) DO NOTHING;

INSERT INTO creatives (
    creative_id,
    campaign_id,
    creative_name,
    media_url,
    duration_seconds,
    creative_type,
    status
)
VALUES
    (
        'creative_streamfuel_15s',
        'camp_streamfuel_live_sports',
        'Stay in the Game',
        'https://cdn.example.com/ads/streamfuel_15s.mp4',
        15,
        'VIDEO',
        'ACTIVE'
    ),
    (
        'creative_quickcart_15s',
        'camp_quickcart_match_day',
        'Snacks Before Overtime',
        'https://cdn.example.com/ads/quickcart_15s.mp4',
        15,
        'VIDEO',
        'ACTIVE'
    ),
    (
        'creative_autosure_30s',
        'camp_autosure_sports_fans',
        'Protected Every Mile',
        'https://cdn.example.com/ads/autosure_30s.mp4',
        30,
        'VIDEO',
        'ACTIVE'
    ),
    (
        'creative_fitpulse_30s',
        'camp_fitpulse_performance',
        'Train Like a Pro',
        'https://cdn.example.com/ads/fitpulse_30s.mp4',
        30,
        'VIDEO',
        'ACTIVE'
    )
ON CONFLICT (creative_id) DO NOTHING;

INSERT INTO placements (
    placement_id,
    placement_name,
    content_type,
    device_type,
    max_ad_duration_seconds,
    status
)
VALUES
    (
        'sports_midroll_001',
        'Live Sports Mid-Roll',
        'LIVE_SPORTS',
        'CTV',
        90,
        'ACTIVE'
    ),
    (
        'sports_preroll_001',
        'Live Sports Pre-Roll',
        'LIVE_SPORTS',
        'CTV',
        30,
        'ACTIVE'
    )
ON CONFLICT (placement_id) DO NOTHING;

INSERT INTO campaign_placements (campaign_id, placement_id)
VALUES
    ('camp_streamfuel_live_sports', 'sports_midroll_001'),
    ('camp_quickcart_match_day', 'sports_midroll_001'),
    ('camp_autosure_sports_fans', 'sports_midroll_001'),
    ('camp_fitpulse_performance', 'sports_midroll_001'),
    ('camp_streamfuel_live_sports', 'sports_preroll_001'),
    ('camp_quickcart_match_day', 'sports_preroll_001')
ON CONFLICT (campaign_id, placement_id) DO NOTHING;