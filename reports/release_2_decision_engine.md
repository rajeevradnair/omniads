# Release 2 — Real-Time Decision Engine

## What Was Built

Release 2 added the core real-time decision engine capabilities:

- Candidate Service
- Frequency Cap Service
- Budget Pacing Service
- Ranking Service
- Ad pod packing
- Multi-ad VAST rendering
- Decision trace summary
- Contract tests
- Smoke test for the full decision path

## Why It Matters

Release 1 proved the basic Gateway → Campaign → Targeting → VAST foundation.

Release 2 makes the platform behave more like a real ad decisioning engine by adding:

- top-K candidate generation
- viewer overexposure prevention
- campaign spend pacing
- auction-style ranking
- duration-aware pod filling

## Current Decision Path

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
Ranking Service
   |
   v
Ad Pod Packer
   |
   v
VAST Service
```