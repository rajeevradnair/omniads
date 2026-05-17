# OmniAds

OmniAds is an AWS-native production-ready real-time OTT ad decisioning platform.

The project models how a server-side ad insertion workflow, such as an AWS MediaTailor-style flow, calls an Ad Decision Server during a live sports ad break and receives a personalized ad response.

## Current Status

Implemented the ADS Gateway foundation:

- FastAPI service
- `/services/ads_gateway/app/api/health` GET endpoint
- `/services/ads_gateway/app/api/ads/decision` POST endpoint
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