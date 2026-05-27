# Release 1 — ADS Foundation

## What Was Built

Release 1 built the core OmniAds microservices foundation:

- ADS Gateway
- Campaign Service
- Targeting Service
- VAST Service
- PostgreSQL campaign schema
- Shared request/response contracts
- Traceable request IDs
- First sample creative metadata
- VAST XML rendering

## Why It Matters

This release proves the basic live sports / OTT ad decisioning flow:

```text
MediaTailor-style request
        |
        v
    ADS Gateway
        |
        v
    Campaign Service
        |
        v
    Targeting Service◊=
        |
        v
    VAST Service
        |
        v
    VAST XML
```