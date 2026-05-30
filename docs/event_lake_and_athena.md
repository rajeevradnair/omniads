# Event Lake and Athena Design

## Purpose

OmniAds emits events so ad decisions can be analyzed, monitored, audited, and used for ML training.

## Current Local Event Lake

The current local implementation writes JSONL files under:

```text
data/synthetic_events/

Supported Event Types:

AD_DECISION_CREATED
VAST_RETURNED
IMPRESSION_RECEIVED
CLICK_RECEIVED
CONVERSION_RECEIVED
NO_FILL_RETURNED
```