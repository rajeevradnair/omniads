# Campaign Data Model

The Campaign Service owns the core advertising metadata used by OmniAds.

## Core Tables

### advertisers

Represents companies buying ads.

Examples:

- StreamFuel Sports Drink
- QuickCart Grocery Delivery
- AutoSure Car Insurance
- FitPulse Smartwatch

### campaigns

Represents an advertiser's ad campaign.

A campaign includes:

- advertiser
- objective
- status
- daily budget
- base CPM bid
- start time
- end time

### creatives

Represents the actual ad media asset.

A creative includes:

- campaign
- creative name
- media URL
- duration
- creative type
- status

### placements

Represents where ads can appear.

Examples:

- live sports mid-roll
- live sports pre-roll

### campaign_placements

Maps campaigns to placements.

This allows one campaign to run on multiple placements and one placement to accept multiple campaigns.

## Why This Matters

Before OmniAds can perform targeting, pacing, frequency capping, ML scoring, or ranking, it needs a reliable list of active campaigns and creatives.

The Campaign Service provides that inventory.