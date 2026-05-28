from pydantic import BaseModel, Field

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign


class BudgetPacingEvaluationRequest(BaseModel):
    """Request sent to Budget Pacing Service."""

    ad_request: AdDecisionRequest
    candidates: list[ActiveCampaign]


class PacingAdjustment(BaseModel):
    """Pacing result for a campaign."""

    campaign_id: str
    creative_id: str
    daily_budget_usd: float
    current_spend_usd: float
    expected_spend_usd: float
    pacing_ratio: float
    pacing_multiplier: float
    status: str
    reasons: list[str] = Field(default_factory=list)


class BudgetPacingBlockedCandidate(BaseModel):
    """Candidate blocked by budget pacing."""

    campaign_id: str
    creative_id: str
    current_spend_usd: float
    daily_budget_usd: float
    reasons: list[str] = Field(default_factory=list)


class BudgetPacingEvaluationResponse(BaseModel):
    """Budget pacing evaluation result."""

    allowed_candidates: list[ActiveCampaign] = Field(default_factory=list)
    pacing_adjustments: list[PacingAdjustment] = Field(default_factory=list)
    blocked_candidates: list[BudgetPacingBlockedCandidate] = Field(default_factory=list)


class BudgetSpendRecordRequest(BaseModel):
    """Request to record estimated campaign spend."""

    campaign_id: str
    creative_id: str
    decision_id: str
    spend_usd: float


class BudgetSpendRecordResponse(BaseModel):
    """Response after recording campaign spend."""

    campaign_id: str
    creative_id: str
    decision_id: str
    new_spend_usd: float