import httpx

from libs.contracts.budget_pacing import PacingAdjustment
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.ranking import RankingRequest, RankingResponse


class RankingServiceClient:
    """HTTP client for talking to Ranking Service."""

    def __init__(self, base_url: str, timeout_seconds: float = 2.0):
        """Initialize the Ranking Service client."""

        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def rank(
        self,
        candidates: list[ActiveCampaign],
        pacing_adjustments: list[PacingAdjustment],
        target_pod_duration_seconds: int = 90,
    ) -> RankingResponse:
        """Rank candidates and return winner plus ranked list."""

        url = f"{self._base_url}/api/v1/ranking/rank"

        payload = RankingRequest(
            candidates=candidates,
            pacing_adjustments=pacing_adjustments,
            target_pod_duration_seconds=target_pod_duration_seconds,
        )

        response = httpx.post(
            url,
            json=payload.model_dump(),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return RankingResponse(**response.json())