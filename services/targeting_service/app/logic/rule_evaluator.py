from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.targeting import (
    RejectedCampaign,
    TargetingEvaluationResponse,
)


CAMPAIGN_TARGETING_RULES: dict[str, dict[str, set[str]]] = {
    "camp_streamfuel_live_sports": {
        "allowed_devices": {"ctv", "mobile"},
        "allowed_geos": {"CA", "TX", "NY"},
        "allowed_placements": {"sports_midroll_001", "sports_preroll_001"},
    },
    "camp_quickcart_match_day": {
        "allowed_devices": {"ctv", "web"},
        "allowed_geos": {"CA", "WA", "OR"},
        "allowed_placements": {"sports_midroll_001", "sports_preroll_001"},
    },
    "camp_autosure_sports_fans": {
        "allowed_devices": {"ctv"},
        "allowed_geos": {"CA", "AZ", "NV"},
        "allowed_placements": {"sports_midroll_001"},
    },
    "camp_fitpulse_performance": {
        "allowed_devices": {"mobile", "web"},
        "allowed_geos": {"CA", "NY"},
        "allowed_placements": {"sports_midroll_001"},
    },
}


def evaluate_targeting(
    ad_request: AdDecisionRequest,
    candidates: list[ActiveCampaign],
) -> TargetingEvaluationResponse:
    """Evaluate campaign candidates against targeting rules.

    Args:
        ad_request: Context from the incoming ad decision request.
        candidates: Active campaigns returned by Campaign Service.

    Returns:
        TargetingEvaluationResponse containing eligible and rejected campaigns.
    """

    eligible_campaigns: list[ActiveCampaign] = []
    rejected_campaigns: list[RejectedCampaign] = []

    for candidate in candidates:
        reasons = _evaluate_single_candidate(
            ad_request=ad_request,
            candidate=candidate,
        )

        if reasons:
            rejected_campaigns.append(
                RejectedCampaign(
                    campaign_id=candidate.campaign_id,
                    creative_id=candidate.creative_id,
                    reasons=reasons,
                )
            )
        else:
            eligible_campaigns.append(candidate)

    return TargetingEvaluationResponse(
        eligible_campaigns=eligible_campaigns,
        rejected_campaigns=rejected_campaigns,
    )


def _evaluate_single_candidate(
    ad_request: AdDecisionRequest,
    candidate: ActiveCampaign,
) -> list[str]:
    """Return targeting rejection reasons for one campaign candidate."""

    rules = CAMPAIGN_TARGETING_RULES.get(candidate.campaign_id)

    if rules is None:
        return ["NO_TARGETING_RULES_FOUND"]

    reasons: list[str] = []

    if ad_request.device.lower() not in rules["allowed_devices"]:
        reasons.append("DEVICE_NOT_ALLOWED")

    if ad_request.geo.upper() not in rules["allowed_geos"]:
        reasons.append("GEO_NOT_ALLOWED")

    if ad_request.placement_id not in rules["allowed_placements"]:
        reasons.append("PLACEMENT_NOT_ALLOWED")

    return reasons