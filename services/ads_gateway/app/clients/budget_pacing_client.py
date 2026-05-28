import httpx

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.campaign import ActiveCampaign
from libs.contracts.budget_pacing import (
    BudgetPacingEvaluationRequest,
    BudgetPacingEvaluationResponse,
    BudgetSpendRecordRequest,
    BudgetSpendRecordResponse,
)


class BudgetPacingServiceClient:
    """HTTP client for talking to Budget Pacing Service."""

    def __init__(self, base_url: str, timeout_seconds: float = 2.0):
        """Initialize the Budget Pacing Service client."""

        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def evaluate(
        self,
        ad_request: AdDecisionRequest,
        candidates: list[ActiveCampaign],
    ) -> BudgetPacingEvaluationResponse:
        """Evaluate candidates against campaign budget pacing."""

        url = f"{self._base_url}/api/v1/pacing/evaluate"

        payload = BudgetPacingEvaluationRequest(
            ad_request=ad_request,
            candidates=candidates,
        )

        response = httpx.post(
            url,
            json=payload.model_dump(),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return BudgetPacingEvaluationResponse(**response.json())

    def record_spend(
        self,
        campaign_id: str,
        creative_id: str,
        decision_id: str,
        spend_usd: float,
    ) -> BudgetSpendRecordResponse:
        """Record estimated spend for the selected campaign."""

        url = f"{self._base_url}/api/v1/pacing/record-spend"

        payload = BudgetSpendRecordRequest(
            campaign_id=campaign_id,
            creative_id=creative_id,
            decision_id=decision_id,
            spend_usd=spend_usd,
        )

        response = httpx.post(
            url,
            json=payload.model_dump(),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return BudgetSpendRecordResponse(**response.json())