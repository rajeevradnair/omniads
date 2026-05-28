from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.budget_pacing import (
    BudgetPacingBlockedCandidate,
    BudgetPacingEvaluationResponse,
    BudgetSpendRecordResponse,
    PacingAdjustment,
)
from services.budget_pacing_service.app.logic.pacing_formula import (
    calculate_day_progress,
    calculate_expected_spend,
    calculate_pacing_ratio,
    determine_pacing_status_and_multiplier,
)
from services.budget_pacing_service.app.repositories.in_memory_budget_repository import (
    InMemoryBudgetRepository,
)


_repository = InMemoryBudgetRepository()


def evaluate_budget_pacing(
    ad_request: AdDecisionRequest,
    candidates: list[ActiveCampaign],
) -> BudgetPacingEvaluationResponse:
    """Evaluate candidates against daily budget pacing state."""

    del ad_request  # Reserved for future regional/event-level pacing.

    allowed_candidates: list[ActiveCampaign] = []
    blocked_candidates: list[BudgetPacingBlockedCandidate] = []
    pacing_adjustments: list[PacingAdjustment] = []

    day_progress = calculate_day_progress()

    for candidate in candidates:
        daily_budget = float(candidate.daily_budget_usd)
        current_spend = _repository.get_spend(candidate.campaign_id)

        # Block the candidate for propagating further as daily budget is exhausted
        if current_spend >= daily_budget:
            blocked_candidates.append(
                BudgetPacingBlockedCandidate(
                    campaign_id=candidate.campaign_id,
                    creative_id=candidate.creative_id,
                    current_spend_usd=current_spend,
                    daily_budget_usd=daily_budget,
                    reasons=["DAILY_BUDGET_EXHAUSTED"],
                )
            )
            continue
        
        # Code for Allowed candidates

        # Calculate expected spend for allowed candidate
        expected_spend = calculate_expected_spend(
            daily_budget_usd=daily_budget,
            day_progress=day_progress,
        )

        # Calculate the pacing ratio for allowed candidate
        pacing_ratio = calculate_pacing_ratio(
            current_spend_usd=current_spend,
            expected_spend_usd=expected_spend,
        )

        status, multiplier, reasons = determine_pacing_status_and_multiplier(
            pacing_ratio=pacing_ratio,
        )

        # Calculate pacing adjustment for allowed candidate
        pacing_adjustments.append(
            PacingAdjustment(
                campaign_id=candidate.campaign_id,
                creative_id=candidate.creative_id,
                daily_budget_usd=daily_budget,
                current_spend_usd=round(current_spend, 6),
                expected_spend_usd=round(expected_spend, 6),
                pacing_ratio=round(pacing_ratio, 4),
                pacing_multiplier=multiplier,
                status=status,
                reasons=reasons,
            )
        )

        allowed_candidates.append(candidate)

    return BudgetPacingEvaluationResponse(
        allowed_candidates=allowed_candidates,
        pacing_adjustments=pacing_adjustments,
        blocked_candidates=blocked_candidates,
    )


def record_budget_spend(
    campaign_id: str,
    creative_id: str,
    decision_id: str,
    spend_usd: float,
) -> BudgetSpendRecordResponse:
    """Record estimated campaign spend."""

    new_spend = _repository.increment_spend(
        campaign_id=campaign_id,
        spend_usd=spend_usd,
    )

    return BudgetSpendRecordResponse(
        campaign_id=campaign_id,
        creative_id=creative_id,
        decision_id=decision_id,
        new_spend_usd=round(new_spend, 6),
    )