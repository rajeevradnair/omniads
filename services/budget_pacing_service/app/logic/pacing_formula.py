from datetime import datetime, timezone


def calculate_day_progress() -> float:
    """Return how much of the UTC day has elapsed as a value from 0 to 1."""

    now = datetime.now(timezone.utc)

    seconds_elapsed = (
        now.hour * 3600
        + now.minute * 60
        + now.second
    )

    seconds_in_day = 24 * 3600

    progress = seconds_elapsed / seconds_in_day

    return max(progress, 0.01)


def calculate_expected_spend(
    daily_budget_usd: float,
    day_progress: float,
) -> float:
    """Return expected spend for the elapsed portion of the day."""

    return daily_budget_usd * day_progress


def calculate_pacing_ratio(
    current_spend_usd: float,
    expected_spend_usd: float,
) -> float:
    """Return actual spend divided by expected spend."""

    if expected_spend_usd <= 0:
        return 0.0

    return current_spend_usd / expected_spend_usd


def determine_pacing_status_and_multiplier(
    pacing_ratio: float,
) -> tuple[str, float, list[str]]:
    """Return pacing status, multiplier, and reasons."""

    if pacing_ratio < 0.85:
        return (
            "UNDERPACED",
            1.15,
            ["CAMPAIGN_UNDERPACED_BOOST_DELIVERY"],
        )

    if pacing_ratio > 1.15:
        return (
            "OVERPACED",
            0.75,
            ["CAMPAIGN_OVERPACED_THROTTLE_DELIVERY"],
        )

    return (
        "ON_TRACK",
        1.0,
        ["CAMPAIGN_ON_TRACK"],
    )


def estimate_impression_cost_from_cpm(base_bid_cpm_usd: float) -> float:
    """Estimate impression cost from CPM bid."""

    return base_bid_cpm_usd / 1000.0