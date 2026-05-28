from fastapi import APIRouter

from libs.contracts.budget_pacing import (
    BudgetPacingEvaluationRequest,
    BudgetPacingEvaluationResponse,
    BudgetSpendRecordRequest,
    BudgetSpendRecordResponse,
)
from services.budget_pacing_service.app.logic.budget_pacing_service import (
    evaluate_budget_pacing,
    record_budget_spend,
)

router = APIRouter()


@router.post(
    "/api/v1/pacing/evaluate",
    response_model=BudgetPacingEvaluationResponse,
)
def evaluate_budget_pacing_endpoint(
    request: BudgetPacingEvaluationRequest,
) -> BudgetPacingEvaluationResponse:
    """Evaluate campaign candidates against budget pacing state."""

    return evaluate_budget_pacing(
        ad_request=request.ad_request,
        candidates=request.candidates,
    )


@router.post(
    "/api/v1/pacing/record-spend",
    response_model=BudgetSpendRecordResponse,
)
def record_budget_spend_endpoint(
    request: BudgetSpendRecordRequest,
) -> BudgetSpendRecordResponse:
    """Record estimated spend for a selected campaign."""

    return record_budget_spend(
        campaign_id=request.campaign_id,
        creative_id=request.creative_id,
        decision_id=request.decision_id,
        spend_usd=request.spend_usd,
    )