from pydantic import BaseModel, Field

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign


class CandidateGenerationRequest(BaseModel):
    """Request sent to Candidate Service for candidate generation."""

    ad_request: AdDecisionRequest
    active_campaigns: list[ActiveCampaign]
    max_candidates: int = 3


class CandidateReason(BaseModel):
    """Reason codes explaining why a campaign became a candidate."""

    campaign_id: str
    creative_id: str
    candidate_score: float
    reasons: list[str] = Field(default_factory=list)


class CandidateGenerationResponse(BaseModel):
    """Candidate Service result."""

    candidates: list[ActiveCampaign] = Field(default_factory=list)
    candidate_reasons: list[CandidateReason] = Field(default_factory=list)

    @property
    def candidate_count(self) -> int:
        """Return number of generated candidates."""
        return len(self.candidates)