from fastapi import APIRouter

from libs.contracts.ranking import RankingRequest, RankingResponse
from services.ranking_service.app.logic.ranking_engine import rank_candidates

router = APIRouter()


@router.post("/api/v1/ranking/rank", response_model=RankingResponse)
def rank_candidates_endpoint(request: RankingRequest) -> RankingResponse:
    """Rank pacing-allowed ad candidates."""

    return rank_candidates(
        candidates=request.candidates,
        pacing_adjustments=request.pacing_adjustments,
        target_pod_duration_seconds=request.target_pod_duration_seconds,
    )