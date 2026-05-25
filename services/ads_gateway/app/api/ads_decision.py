from fastapi import APIRouter, HTTPException
from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.ad_response import AdDecisionResponse

import httpx

from libs.contracts.campaign import ActiveCampaign

from services.ads_gateway.app.clients.campaign_client import CampaignServiceClient
from services.ads_gateway.app.config import get_campaign_service_url
from services.ads_gateway.app.orchestration.trace_context import create_decision_trace

router = APIRouter()

@router.post("/api/v1/ads_gateway/ads/decision")
def create_ad_decision(request: AdDecisionRequest) -> AdDecisionResponse:
    
    trace = create_decision_trace()

    campaign_client = CampaignServiceClient(
        base_url=get_campaign_service_url()
    )
    
    print(campaign_client.base_url, request.placement_id)

    try:
        active_campaigns:list[ActiveCampaign] = campaign_client.list_active_campaigns(
            placement_id=request.placement_id
        )
    except httpx.HTTPError as exec:
        raise HTTPException(
            status_code=502,
            detail=(
                "ADS Gateway could not retrieve active campaigns "
                f"from Campaign Service: {exec}"
            ),
        ) from exec

    num_active_campaigns = len(active_campaigns)
    if num_active_campaigns > 0:
        selected_campaign:ActiveCampaign = active_campaigns[0]
        return AdDecisionResponse(
            request_id=trace.request_id,
            trace_id=trace.trace_id,
            decision_id=trace.decision_id,
            selected_campaign_id=selected_campaign.campaign_id,
            selected_creative_id=selected_campaign.creative_id,
            status="CAMPAIGN_SERVICE_DECISION_RETURNED",
            reason="Ad decision returned the first in the list of campaigns sorted by base_bid_cpm_usd",
            candidate_count=num_active_campaigns,
            candidate_campaign_ids=[campaign.campaign_id for campaign in active_campaigns]
        )        
    else:
                return AdDecisionResponse(
            request_id=trace.request_id,
            trace_id=trace.trace_id,
            decision_id=trace.decision_id,
            selected_campaign_id=None,
            selected_creative_id=None,
            status="NO_FILL",
            reason=(
                "No active campaigns returned by Campaign Service for "
                f"placement_id={request.placement_id}."
            ),
            candidate_count=0,
            candidate_campaign_ids=[],
        )

