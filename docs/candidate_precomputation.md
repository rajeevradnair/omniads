# Candidate Generation and Precomputation

## Current Candidate Generation

The Candidate Service reduces active campaigns into a smaller top-K candidate set.

Current input:

- ad request context
- active campaigns from Campaign Service
- max candidate count

Current output:

- generated candidates
- candidate reason codes
- simple candidate score

## Why Candidate Generation Matters

Real ad platforms cannot deeply evaluate every campaign for every ad request.

Candidate generation narrows the campaign pool before targeting, frequency caps, pacing, scoring, and ranking.

## Current Heuristics

The current implementation uses simple deterministic heuristics:

- base CPM bid
- live sports mid-roll placement match
- supported creative duration
- campaign objective bonus

## Future Design

Later releases will move toward:

- Redis cached candidate sets
- precomputed candidates by placement, geography, content genre, and viewer segment
- candidate invalidation when campaign metadata changes
- cache hit/miss metrics