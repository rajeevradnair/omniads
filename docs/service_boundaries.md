# Service Boundaries

OmniAds is designed as a microservices-based ad decisioning platform.

## ADS Gateway Responsibility

The ADS Gateway is the public entry point for MediaTailor-style ad requests.

It owns:

- request validation
- request_id, trace_id, and decision_id creation
- downstream service orchestration
- final response assembly

It does not own campaign metadata.

## Campaign Service Responsibility

The Campaign Service owns campaign inventory metadata.

It owns:

- advertisers
- campaigns
- creatives
- placements
- campaign-to-placement eligibility

## Why This Boundary Matters

Ad decisioning requires multiple independent business capabilities.

Keeping campaign metadata in a separate service makes it easier to:

- scale campaign lookup independently
- cache campaign metadata later
- evolve campaign schema without changing Gateway logic
- keep the Gateway focused on orchestration