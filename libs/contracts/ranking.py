from pydantic import BaseModel, Field

from libs.contracts.budget_pacing import PacingAdjustment
from libs.contracts.campaign import ActiveCampaign


class RankingRequest(BaseModel):
    """Request sent to Ranking Service."""

    candidates: list[ActiveCampaign]
    pacing_adjustments: list[PacingAdjustment] = Field(default_factory=list)


class RankedCandidate(BaseModel):
    """One ranked ad candidate."""

    campaign_id: str
    creative_id: str
    creative_name: str
    advertiser_name: str
    base_bid_cpm_usd: float
    pacing_multiplier: float
    objective_weight: float
    final_score: float
    rank: int
    reasons: list[str] = Field(default_factory=list)


class RankingResponse(BaseModel):
    """Ranking result."""

    winner: RankedCandidate | None = None
    ranked_candidates: list[RankedCandidate] = Field(default_factory=list)