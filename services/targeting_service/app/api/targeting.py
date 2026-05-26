from fastapi import APIRouter

from libs.contracts.targeting import TargetingEvaluationRequest, TargetingEvaluationResponse
from services.targeting_service.app.logic.rule_evaluator import evaluate_targeting


router = APIRouter()

@router.post("/api/v1/targeting/evaluate", response_model=TargetingEvaluationResponse)
def evaluate_targeting_endpoint(request: TargetingEvaluationRequest) -> TargetingEvaluationResponse:
    return evaluate_targeting(
        request.ad_request,
        request.candidates,
    )

