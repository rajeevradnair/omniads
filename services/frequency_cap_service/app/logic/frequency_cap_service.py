from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.frequency_cap import (
    FrequencyCapBlockedCandidate,
    FrequencyCapEvaluationResponse,
    FrequencyCapRecordResponse,
)
from services.frequency_cap_service.app.repositories.in_memory_frequency_cap_repository import (
    InMemoryFrequencyCapRepository,
)


_repository = InMemoryFrequencyCapRepository()


def evaluate_frequency_caps(
    ad_request: AdDecisionRequest,
    candidates: list[ActiveCampaign],
    max_daily_impressions_per_creative: int,
) -> FrequencyCapEvaluationResponse:
    """Evaluate candidates against viewer-creative daily frequency caps."""

    allowed_candidates: list[ActiveCampaign] = []
    blocked_candidates: list[FrequencyCapBlockedCandidate] = []

    for candidate in candidates:
        current_count = _repository.get_count(
            viewer_id=ad_request.viewer_id,
            creative_id=candidate.creative_id,
        )

        if current_count >= max_daily_impressions_per_creative:
            blocked_candidates.append(
                FrequencyCapBlockedCandidate(
                    campaign_id=candidate.campaign_id,
                    creative_id=candidate.creative_id,
                    current_count=current_count,
                    max_allowed=max_daily_impressions_per_creative,
                    reasons=["VIEWER_CREATIVE_DAILY_CAP_REACHED"],
                )
            )
        else:
            allowed_candidates.append(candidate)

    return FrequencyCapEvaluationResponse(
        allowed_candidates=allowed_candidates,
        blocked_candidates=blocked_candidates,
    )


def record_frequency_cap_exposure(
    viewer_id: str,
    campaign_id: str,
    creative_id: str,
    decision_id: str,
) -> FrequencyCapRecordResponse:
    """Record that a selected creative exposure occurred."""

    new_count = _repository.increment_count(
        viewer_id=viewer_id,
        creative_id=creative_id,
    )

    return FrequencyCapRecordResponse(
        viewer_id=viewer_id,
        campaign_id=campaign_id,
        creative_id=creative_id,
        new_count=new_count,
    )