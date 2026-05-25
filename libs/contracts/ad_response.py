from typing import Optional

from pydantic import BaseModel, Field

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