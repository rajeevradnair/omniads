import httpx

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.candidate import (
    CandidateGenerationRequest,
    CandidateGenerationResponse,
)


class CandidateServiceClient:
    """HTTP client for talking to Candidate Service."""

    def __init__(self, base_url: str, timeout_seconds: float = 2.0):
        """Initialize the Candidate Service client."""

        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def generate(
        self,
        ad_request: AdDecisionRequest,
        active_campaigns: list[ActiveCampaign],
        max_candidates: int = 3,
    ) -> CandidateGenerationResponse:
        """Generate top-K candidates from active campaigns."""

        url = f"{self._base_url}/api/v1/candidates/generate"

        payload = CandidateGenerationRequest(
            ad_request=ad_request,
            active_campaigns=active_campaigns,
            max_candidates=max_candidates,
        )

        response = httpx.post(
            url,
            json=payload.model_dump(),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return CandidateGenerationResponse(**response.json())