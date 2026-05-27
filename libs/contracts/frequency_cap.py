from pydantic import BaseModel, Field

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign


class FrequencyCapEvaluationRequest(BaseModel):
    """Request sent to Frequency Cap Service for cap evaluation."""

    ad_request: AdDecisionRequest
    candidates: list[ActiveCampaign]
    max_daily_impressions_per_creative: int = 3


class FrequencyCapBlockedCandidate(BaseModel):
    """Candidate blocked by frequency cap rules."""

    campaign_id: str
    creative_id: str
    current_count: int
    max_allowed: int
    reasons: list[str] = Field(default_factory=list)


class FrequencyCapEvaluationResponse(BaseModel):
    """Frequency cap evaluation result."""

    allowed_candidates: list[ActiveCampaign] = Field(default_factory=list)
    blocked_candidates: list[FrequencyCapBlockedCandidate] = Field(default_factory=list)

    @property
    def allowed_count(self) -> int:
        """Return number of candidates allowed by frequency capping."""
        return len(self.allowed_candidates)

    @property
    def blocked_count(self) -> int:
        """Return number of candidates blocked by frequency capping."""
        return len(self.blocked_candidates)


class FrequencyCapRecordRequest(BaseModel):
    """Request to record that a creative exposure occurred."""

    viewer_id: str
    campaign_id: str
    creative_id: str
    decision_id: str


class FrequencyCapRecordResponse(BaseModel):
    """Response after recording a creative exposure."""

    viewer_id: str
    campaign_id: str
    creative_id: str
    new_count: int