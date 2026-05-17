# OmniAds Architecture

## Current Architecture

```text
MediaTailor-style Request
        |
        v
ADS Gateway
        |
        v
Mock Ad Decision Response
```

## Future Architecture

```text
ADS Gateway
   |
   |-- Campaign Service
   |-- Candidate Service
   |-- Targeting Service
   |-- Frequency Cap Service
   |-- Budget Pacing Service
   |-- Scoring Service
   |-- Ranking Service
   |-- VAST Service
   |-- Event Logging Service
```