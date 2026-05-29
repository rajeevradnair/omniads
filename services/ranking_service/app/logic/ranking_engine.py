from libs.contracts.budget_pacing import PacingAdjustment
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.ranking import RankedCandidate, RankingResponse
from services.ranking_service.app.logic.ad_pod_packer import pack_ad_pod

def rank_candidates(
    candidates: list[ActiveCampaign],
    pacing_adjustments: list[PacingAdjustment],
    target_pod_duration_seconds: int = 90,
) -> RankingResponse:
    """Rank candidates using a simple eCPM-style scoring formula."""

    pacing_lookup = _build_pacing_lookup(pacing_adjustments)
    scored_candidates: list[RankedCandidate] = []

    for candidate in candidates:
        pacing_multiplier = pacing_lookup.get(
            _candidate_key(candidate.campaign_id, candidate.creative_id),
            1.0,
        )

        objective_weight = _objective_weight(candidate.objective)

        final_score = (
            float(candidate.base_bid_cpm_usd)
            * pacing_multiplier
            * objective_weight
        )

        scored_candidates.append(
            RankedCandidate(
                campaign_id=candidate.campaign_id,
                creative_id=candidate.creative_id,
                creative_name=candidate.creative_name,
                advertiser_name=candidate.advertiser_name,
                media_url=candidate.media_url,
                duration_seconds=candidate.duration_seconds,
                base_bid_cpm_usd=float(candidate.base_bid_cpm_usd),
                pacing_multiplier=pacing_multiplier,
                objective_weight=objective_weight,
                final_score=round(final_score, 6),
                rank=0,
                reasons=[
                    "BASE_BID_INCLUDED",
                    "PACING_MULTIPLIER_APPLIED",
                    "OBJECTIVE_WEIGHT_APPLIED",
                ],
            )
        )

    scored_candidates.sort(
        key=lambda candidate: candidate.final_score,
        reverse=True,
    )

    ranked_candidates = [
        candidate.model_copy(update={"rank": index + 1})
        for index, candidate in enumerate(scored_candidates)
    ]

    packed_ad_pod = pack_ad_pod(
        ranked_candidates=ranked_candidates, 
        target_duration_seconds=target_pod_duration_seconds
    )

    winner = ranked_candidates[0] if ranked_candidates else None

    return RankingResponse(
        winner=winner,
        ranked_candidates=ranked_candidates,
        packed_ad_pod=packed_ad_pod,
    )


def _build_pacing_lookup(
    pacing_adjustments: list[PacingAdjustment],
) -> dict[str, float]:
    """Build campaign-creative lookup for pacing multipliers."""

    lookup: dict[str, float] = {}

    for adjustment in pacing_adjustments:
        key = _candidate_key(
            campaign_id=adjustment.campaign_id,
            creative_id=adjustment.creative_id,
        )
        lookup[key] = adjustment.pacing_multiplier

    return lookup


def _candidate_key(campaign_id: str, creative_id: str) -> str:
    """Return stable key for campaign creative pair."""

    return f"{campaign_id}::{creative_id}"


def _objective_weight(objective: str) -> float:
    """Return a simple ranking weight for a campaign objective."""

    objective_upper = objective.upper()

    if objective_upper == "CONVERSION":
        return 1.20

    if objective_upper == "CONSIDERATION":
        return 1.10

    if objective_upper == "LEAD_GENERATION":
        return 1.05

    if objective_upper == "AWARENESS":
        return 1.00

    return 1.00