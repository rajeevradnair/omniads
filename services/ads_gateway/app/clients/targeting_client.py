import httpx

from libs.contracts.campaign import ActiveCampaign
from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.targeting import (
    TargetingEvaluationRequest,
    TargetingEvaluationResponse,
)


class TargetingServiceClient:
    def __init__(self, base_url: str, timeout_seconds:float = 2.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def evaluate(self, ad_request: AdDecisionRequest, candidates: list[ActiveCampaign]) -> TargetingEvaluationResponse:
        url = self.base_url + "/api/v1/targeting/evaluate"

        targeting_evaluation_request = TargetingEvaluationRequest(
            ad_request=ad_request,
            candidates=candidates,
        )

        response = httpx.post(
            url,
            json=targeting_evaluation_request.model_dump(),
            timeout=self.timeout_seconds,
        )

        response.raise_for_status()
        response_payload = response.json()

        return TargetingEvaluationResponse(**response_payload)
