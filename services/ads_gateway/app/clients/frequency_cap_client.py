import httpx

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.frequency_cap import (
    FrequencyCapEvaluationRequest,
    FrequencyCapEvaluationResponse,
    FrequencyCapRecordRequest,
    FrequencyCapRecordResponse,
)


class FrequencyCapServiceClient:
    """HTTP client for talking to Frequency Cap Service."""

    def __init__(self, base_url: str, timeout_seconds: float = 2.0):
        """Initialize the Frequency Cap Service client."""

        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def evaluate(
        self,
        ad_request: AdDecisionRequest,
        candidates: list[ActiveCampaign],
        max_daily_impressions_per_creative: int = 3,
    ) -> FrequencyCapEvaluationResponse:
        """Evaluate candidates against frequency caps."""

        url = f"{self._base_url}/api/v1/frequency_caps/evaluate"

        payload = FrequencyCapEvaluationRequest(
            ad_request=ad_request,
            candidates=candidates,
            max_daily_impressions_per_creative=(
                max_daily_impressions_per_creative
            ),
        )

        response = httpx.post(
            url,
            json=payload.model_dump(),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return FrequencyCapEvaluationResponse(**response.json())

    def record(
        self,
        viewer_id: str,
        campaign_id: str,
        creative_id: str,
        decision_id: str,
    ) -> FrequencyCapRecordResponse:
        """Record a selected creative exposure."""

        url = f"{self._base_url}/api/v1/frequency_caps/record"

        payload = FrequencyCapRecordRequest(
            viewer_id=viewer_id,
            campaign_id=campaign_id,
            creative_id=creative_id,
            decision_id=decision_id,
        )

        response = httpx.post(
            url,
            json=payload.model_dump(),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return FrequencyCapRecordResponse(**response.json())