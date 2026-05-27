from fastapi import APIRouter

from libs.contracts.frequency_cap import (
    FrequencyCapEvaluationRequest,
    FrequencyCapEvaluationResponse,
    FrequencyCapRecordRequest,
    FrequencyCapRecordResponse,
)
from services.frequency_cap_service.app.logic.frequency_cap_service import (
    evaluate_frequency_caps,
    record_frequency_cap_exposure,
)

router = APIRouter()


@router.post(
    "/api/v1/frequency_caps/evaluate",
    response_model=FrequencyCapEvaluationResponse,
)
def evaluate_frequency_caps_endpoint(
    request: FrequencyCapEvaluationRequest,
) -> FrequencyCapEvaluationResponse:
    """Evaluate candidate creatives against viewer frequency caps."""

    return evaluate_frequency_caps(
        ad_request=request.ad_request,
        candidates=request.candidates,
        max_daily_impressions_per_creative=(
            request.max_daily_impressions_per_creative
        ),
    )


@router.post(
    "/api/v1/frequency_caps/record",
    response_model=FrequencyCapRecordResponse,
)
def record_frequency_cap_endpoint(
    request: FrequencyCapRecordRequest,
) -> FrequencyCapRecordResponse:
    """Record a selected creative exposure."""

    return record_frequency_cap_exposure(
        viewer_id=request.viewer_id,
        campaign_id=request.campaign_id,
        creative_id=request.creative_id,
        decision_id=request.decision_id,
    )