from pydantic import BaseModel, Field

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign

class TargetingEvaluationRequest(BaseModel):
    ad_request:AdDecisionRequest
    candidates: list[ActiveCampaign]


class RejectedCampaign(BaseModel):
    campaign_id: str
    creative_id: str
    reasons: list[str] = Field(default_factory = list)


class TargetingEvaluationResponse(BaseModel):
    eligible_campaigns: list[ActiveCampaign]
    rejected_campaigns: list[RejectedCampaign]

    def eligible_count(self) -> int:
        return len(self.eligible_campaigns)
    
    def rejected_count(self) -> int:
        return len(self.rejected_campaigns)

