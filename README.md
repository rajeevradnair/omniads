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

## Service-to-Service Campaign Lookup

The ADS Gateway calls Campaign Service over HTTP.

Current flow:

```text
POST /ads/decision
        |
        v
ADS Gateway
        |
        v
GET /campaigns/active?placement_id=...
        |
        v
Campaign Service
        |
        v
PostgreSQL
```

The Gateway temporarily selects the first active campaign returned by Campaign Service. Future releases will replace this temporary selection with targeting, pacing, scoring, ranking, and VAST generation.

## Targeting Service

The Targeting Service evaluates whether active campaign candidates are eligible for a specific ad request.

Current flow:

```text
ADS Gateway
   |
   v
Campaign Service
   |
   v
Targeting Service
   |
   v
Eligible campaigns + rejection reasons
```

## Candidate Service

The Candidate Service was added in Release 2 to reduce active campaigns into a smaller top-K candidate set.

Current flow:

```text
ADS Gateway
   |
   v
Campaign Service
   |
   v
Candidate Service
   |
   v
Targeting Service
   |
   v
VAST Service
```

## Frequency Cap Service

The Frequency Cap Service was added in Release 2 to prevent overexposure.

Current endpoints:

- `GET /api/v1/frequency_caps/health`
- `POST /api/v1/frequency_caps/frequency-caps/evaluate`
- `POST /api/v1/frequency_caps/frequency-caps/record`

Current flow:

```text
ADS Gateway
   |
   v
Campaign Service
   |
   v
Candidate Service
   |
   v
Targeting Service
   |
   v
Frequency Cap Service
   |
   v
VAST Service
```

## Budget Pacing Service

The Budget Pacing Service was added in Release 2 to prevent campaign overspend and support delivery control.

Current endpoints:

- `GET /api/v1/pacing/health`
- `POST /api/v1/pacing/evaluate`
- `POST /api/v1/pacing/record-spend`

Current flow:

```text
ADS Gateway
   |
   v
Campaign Service
   |
   v
Candidate Service
   |
   v
Targeting Service
   |
   v
Frequency Cap Service
   |
   v
Budget Pacing Service
   |
   v
VAST Service
```