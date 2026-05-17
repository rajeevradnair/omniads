# Request Tracing

Every ad decision must be traceable across services.

OmniAds starts with three identifiers:

## request_id

Identifies the API request received by the ADS Gateway.

## trace_id

Connects logs across future microservices.

## decision_id

Identifies the final ad decision.

Future services will include these IDs in all logs:

- ADS Gateway
- Campaign Service
- Candidate Service
- Targeting Service
- Frequency Cap Service
- Budget Pacing Service
- Scoring Service
- Ranking Service
- VAST Service
- Event Logging Service