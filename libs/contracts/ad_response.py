from typing import Optional

from pydantic import BaseModel, Field

from libs.contracts.targeting import RejectedCampaign
from libs.contracts.candidate import CandidateReason
from libs.contracts.frequency_cap import FrequencyCapBlockedCandidate
from libs.contracts.budget_pacing import BudgetPacingBlockedCandidate, PacingAdjustment
from libs.contracts.ranking import RankedCandidate
from libs.contracts.ranking import PackedAdPod

# Flow: 
# active campaigns (campaign_service) 
# → generated candidates (candidate service) 
# → eligible candidates (targeting service)

class AdDecisionResponse(BaseModel):
    request_id: str
    trace_id: str
    decision_id: str
    selected_campaign_id: Optional[str]
    selected_creative_id: Optional[str]
    status: str
    reason: str
    candidate_count: int = 0
    candidate_campaign_ids: list[str] = Field(default_factory=list)
    generated_candidate_count: int = 0
    generated_candidate_campaign_ids: list[str] = Field(default_factory=list)
    candidate_reasons: list[CandidateReason] = Field(default_factory=list)    
    eligible_candidate_count: int = 0
    eligible_campaign_ids: list[str] = Field(default_factory=list)
    rejected_campaigns: list[RejectedCampaign] = Field(default_factory=list)
    frequency_cap_allowed_count: int = 0
    frequency_cap_allowed_campaign_ids: list[str] = Field(default_factory=list)
    frequency_cap_blocked: list[FrequencyCapBlockedCandidate] = Field(default_factory=list)
    frequency_cap_recorded_count: int | None = None
    pacing_allowed_count: int = 0
    pacing_allowed_campaign_ids: list[str] = Field(default_factory=list)
    pacing_adjustments: list[PacingAdjustment] = Field(default_factory=list)
    pacing_blocked: list[BudgetPacingBlockedCandidate] = Field(default_factory=list)
    budget_spend_recorded_usd: float | None = None
    campaign_new_spend_usd: float | None = None
    ranking_winner: RankedCandidate | None = None
    ranked_candidates: list[RankedCandidate] = Field(default_factory=list)
    packed_ad_pod: PackedAdPod | None = None
    vast_xml: Optional[str] = None
