# Timeout Policy

OmniAds is a real-time ad decisioning simulation. The ADS Gateway must not wait indefinitely for downstream services.

## Current Local Defaults

Each service client currently uses a local development timeout of approximately 2 seconds (too generous).

## Future Production Targets

| Dependency | Future Target Timeout |
|---|---:|
| Campaign Service | 50–100 ms |
| Candidate Service | 25–75 ms |
| Targeting Service | 25–75 ms |
| Frequency Cap Service | 25–75 ms |
| Budget Pacing Service | 25–75 ms |
| Ranking Service | 10–50 ms |
| VAST Service | 25–100 ms |

## Timeout Behavior

If a required dependency fails, ADS Gateway returns a 502 dependency error.

Future releases needs to add graceful fallbacks such as:

- cached campaign candidates
- default targeting pass/fail behavior
- fallback slate VAST
- no-fill response
- degraded scoring mode