from fastapi import APIRouter
from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.ad_response import AdDecisionResponse

from services.ads_gateway.app.orchestration.trace_context import create_decision_trace

router = APIRouter()

@router.post("/api/v1/ads_gateway/ads/decision")
def create_ad_decision(request: AdDecisionRequest) -> AdDecisionResponse:
    
    trace = create_decision_trace()

    #print(trace)

    return AdDecisionResponse(
        request_id=trace.request_id,
        trace_id=trace.trace_id,
        decision_id=trace.decision_id,
        selected_campaign_id="campaign_001",
        selected_creative_id="creative_001",
        status="DECISION_RETURNED",
        reason="Ad decision returned by ADS Gateway",
    )