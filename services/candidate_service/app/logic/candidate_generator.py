from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.candidate import (
    CandidateGenerationResponse,
    CandidateReason,
)


def generate_candidates(
    ad_request: AdDecisionRequest,
    active_campaigns: list[ActiveCampaign],
    max_candidates: int,
) -> CandidateGenerationResponse:
    """Generate a top-K candidate set from active campaigns."""

    scored_candidates: list[tuple[ActiveCampaign, CandidateReason]] = []

    for campaign in active_campaigns:
        score, reasons = _score_candidate(
            ad_request=ad_request,
            campaign=campaign,
        )

        scored_candidates.append(
            (
                campaign,
                CandidateReason(
                    campaign_id=campaign.campaign_id,
                    creative_id=campaign.creative_id,
                    candidate_score=score,
                    reasons=reasons,
                ),
            )
        )

    scored_candidates.sort(
        key=lambda item: item[1].candidate_score,
        reverse=True,
    )

    top_scored_candidates = scored_candidates[:max_candidates]

    return CandidateGenerationResponse(
        candidates=[item[0] for item in top_scored_candidates],
        candidate_reasons=[item[1] for item in top_scored_candidates],
    )


def _score_candidate(
    ad_request: AdDecisionRequest,
    campaign: ActiveCampaign,
) -> tuple[float, list[str]]:
    """Assign a simple retrieval score and reason codes to one campaign."""

    score = 0.0
    reasons: list[str] = []

    score += float(campaign.base_bid_cpm_usd)
    reasons.append("BASE_BID_INCLUDED")

    if ad_request.placement_id == "sports_midroll_001":
        score += 5.0
        reasons.append("MATCHES_LIVE_SPORTS_MIDROLL")

    if campaign.duration_seconds in {15, 30}:
        score += 2.0
        reasons.append("SUPPORTED_CREATIVE_DURATION")

    objective_bonus = _objective_bonus(campaign.objective)
    score += objective_bonus

    if objective_bonus > 0:
        reasons.append(f"OBJECTIVE_BONUS_{campaign.objective}")

    return score, reasons


def _objective_bonus(objective: str) -> float:
    """Return a simple candidate-generation bonus by campaign objective."""

    objective_upper = objective.upper()

    if objective_upper == "CONVERSION":
        return 4.0

    if objective_upper == "CONSIDERATION":
        return 3.0

    if objective_upper == "AWARENESS":
        return 2.0

    if objective_upper == "LEAD_GENERATION":
        return 2.5

    return 0.0