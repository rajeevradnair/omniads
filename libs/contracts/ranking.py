from pydantic import BaseModel, Field

from libs.contracts.budget_pacing import PacingAdjustment
from libs.contracts.campaign import ActiveCampaign


class RankingRequest(BaseModel):
    """Request sent to Ranking Service."""

    candidates: list[ActiveCampaign]
    pacing_adjustments: list[PacingAdjustment] = Field(default_factory=list)
    target_pod_duration_seconds: int = 90

class RankedCandidate(BaseModel):
    """One ranked ad candidate."""

    campaign_id: str
    creative_id: str
    creative_name: str
    advertiser_name: str
    media_url: str
    duration_seconds: int
    base_bid_cpm_usd: float
    pacing_multiplier: float
    objective_weight: float
    final_score: float
    rank: int
    reasons: list[str] = Field(default_factory=list)
    

class PackedAdPod(BaseModel):
    """Duration-constrained group of ads selected for an ad break."""

    selected_ads: list[RankedCandidate] = Field(default_factory=list)
    target_duration_seconds: int
    filled_duration_seconds: int
    remaining_duration_seconds: int
    fill_rate: float
    reasons: list[str] = Field(default_factory=list)

class RankingResponse(BaseModel):
    """Ranking result."""

    winner: RankedCandidate | None = None
    ranked_candidates: list[RankedCandidate] = Field(default_factory=list)
    packed_ad_pod: PackedAdPod | None = None
