# Targeting and Pacing

## Targeting

Targeting determines whether an active campaign is eligible for a specific ad request.

The Campaign Service answers:

> Which campaigns are active for this placement?

The Targeting Service answers:

> Which active campaigns are allowed for this viewer, device, geography, placement, and context?

## Current Targeting Rules

Current rules include:

- allowed devices
- allowed geographies
- allowed placements

## Reason Codes

Rejected campaigns return reason codes such as:

- DEVICE_NOT_ALLOWED
- GEO_NOT_ALLOWED
- PLACEMENT_NOT_ALLOWED
- NO_TARGETING_RULES_FOUND

## Why Reason Codes Matter

Reason codes make the ad decision explainable.

Instead of saying:

> No ad was selected.

OmniAds can say:

> Campaign A was rejected because the device was not allowed.
> Campaign B was rejected because the geography was not allowed.

This is important for debugging, campaign operations, and advertiser trust.

## Pacing

Budget pacing will be added later.

Pacing will answer:

> Is the campaign spending too quickly or too slowly relative to its budget and time remaining?

## Budget Pacing

Budget pacing prevents campaigns from spending too quickly or too slowly.

The Budget Pacing Service compares:

```text
actual spend so far
expected spend so far
```