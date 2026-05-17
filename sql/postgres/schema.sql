CREATE TABLE IF NOT EXISTS advertisers (
    advertiser_id TEXT PRIMARY KEY,
    advertiser_name TEXT NOT NULL,
    industry TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
/*
objective: awareness, clicks, conversions, app_installs, brand_lift, subscription_signups
status: DRAFT, ACTIVE. PAUSED, ENDED, ARCHIVED
*/
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id TEXT PRIMARY KEY,
    advertiser_id TEXT NOT NULL REFERENCES advertisers(advertiser_id),
    campaign_name TEXT NOT NULL,
    objective TEXT NOT NULL,
    status TEXT NOT NULL,
    daily_budget_usd NUMERIC(12, 2) NOT NULL,
    base_bid_cpm_usd NUMERIC(12, 4) NOT NULL,
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

/*
creative_type: video/mp4, video, display, audio, vast
status: ACTIVE. PAUSED, REJECTED, PENDING_REVIEW, ARCHIVED
*/
CREATE TABLE IF NOT EXISTS creatives (
    creative_id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL REFERENCES campaigns(campaign_id),
    creative_name TEXT NOT NULL,
    media_url TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    creative_type TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

/*
content_type: sports, news, family, entertainment, movies, live_sports
device_type: ctv, mobile, web, tablet
status: ACTIVE, INACTIVE, DEPRECATED
*/
CREATE TABLE IF NOT EXISTS placements (
    placement_id TEXT PRIMARY KEY,
    placement_name TEXT NOT NULL,
    content_type TEXT NOT NULL,
    device_type TEXT NOT NULL,
    max_ad_duration_seconds INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS campaign_placements (
    campaign_id TEXT NOT NULL REFERENCES campaigns(campaign_id),
    placement_id TEXT NOT NULL REFERENCES placements(placement_id),
    PRIMARY KEY (campaign_id, placement_id)
);

CREATE INDEX IF NOT EXISTS idx_campaigns_status_time
ON campaigns(status, starts_at, ends_at);

CREATE INDEX IF NOT EXISTS idx_creatives_campaign_id
ON creatives(campaign_id);

CREATE INDEX IF NOT EXISTS idx_campaign_placements_placement_id
ON campaign_placements(placement_id);