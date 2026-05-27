from fastapi import APIRouter

from libs.contracts.candidate import (
    CandidateGenerationRequest,
    CandidateGenerationResponse,
)
from services.candidate_service.app.logic.candidate_generator import (
    generate_candidates,
)

router = APIRouter()


@router.post("/api/v1/candidates/generate", response_model=CandidateGenerationResponse)
def generate_candidates_endpoint(
    request: CandidateGenerationRequest,
) -> CandidateGenerationResponse:
    """Generate candidate campaigns from active campaigns."""

    return generate_candidates(
        ad_request=request.ad_request,
        active_campaigns=request.active_campaigns,
        max_candidates=request.max_candidates,
    )