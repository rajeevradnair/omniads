from typing import Optional

from pydantic import BaseModel, Field

from libs.contracts.targeting import RejectedCampaign


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
    eligible_candidate_count: int = 0
    eligible_campaign_ids: list[str] = Field(default_factory=list)
    rejected_campaigns: list[RejectedCampaign] = Field(default_factory=list)
    vast_xml: Optional[str] = None