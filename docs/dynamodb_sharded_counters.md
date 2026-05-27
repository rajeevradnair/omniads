# DynamoDB Frequency Cap Counters

## Purpose

Frequency capping prevents the same viewer from seeing the same creative too many times within a time window.

## Current Local Implementation

The current Frequency Cap Service uses an in-memory repository that simulates DynamoDB-style counters.

Current key shape:

```text
VIEWER#<viewer_id>#CREATIVE#<creative_id>#DAY#<yyyy-mm-dd>
```

Furure key shape:

```text
pk = VIEWER#viewer_123
sk = CREATIVE#creative_streamfuel_15s#DAY#2026-05-27
```