def estimate_impression_cost_from_cpm(base_bid_cpm_usd: float) -> float:
    """Estimate impression-level spend from CPM."""

    return base_bid_cpm_usd / 1000.0