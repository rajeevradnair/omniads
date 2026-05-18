# OmniAds

OmniAds is an AWS-native production-ready real-time OTT ad decisioning platform.

The project models how a server-side ad insertion workflow, such as an AWS MediaTailor-style flow, calls an Ad Decision Server during a live sports ad break and receives a personalized ad response.

## Current Status

Implemented the ADS Gateway foundation:

- FastAPI service
- `GET  /api/v1/ads_gateway/health`
- `POST /api/v1/ads_gateway/ads/decision`
- Ad decision request contract
- Ad decision response contract
- Request, trace, and decision ID generation
- Docker Compose local run path

## Current Demo

A mock MediaTailor-style request enters the ADS Gateway. The gateway creates:

- `request_id`
- `trace_id`
- `decision_id`

Then returns a mock campaign and creative decision.

## Campaign Service

The Campaign Service was added to own advertiser, campaign, creative, and placement metadata.

Current endpoints:

- `GET /api/v1/campaigns/health`
- `GET /api/v1/campaigns/active?placement_id=sports_midroll_001`

The service uses PostgreSQL locally through Docker Compose.

Current data model:

- advertisers
- campaigns
- creatives
- placements
- campaign_placements