import httpx
from fastapi import APIRouter, HTTPException

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.ad_response import AdDecisionResponse
from services.ads_gateway.app.clients.campaign_client import CampaignServiceClient
from services.ads_gateway.app.clients.targeting_client import TargetingServiceClient
from services.ads_gateway.app.config import (
    get_campaign_service_url,
    get_targeting_service_url,
)
from services.ads_gateway.app.orchestration.trace_context import (
    create_decision_trace,
)

router = APIRouter()


@router.post("/api/v1/ads_gateway/ads/decision", response_model=AdDecisionResponse)
def create_ad_decision(request: AdDecisionRequest) -> AdDecisionResponse:
    """Create an ad decision using Campaign and Targeting services."""

    trace = create_decision_trace()

    campaign_client = CampaignServiceClient(
        base_url=get_campaign_service_url(),
    )
    targeting_client = TargetingServiceClient(
        base_url=get_targeting_service_url(),
    )

    try:
        active_campaigns = campaign_client.list_active_campaigns(
            placement_id=request.placement_id,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "ADS Gateway could not retrieve active campaigns "
                f"from Campaign Service: {exc}"
            ),
        ) from exc

    if not active_campaigns:
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
            eligible_candidate_count=0,
            eligible_campaign_ids=[],
            rejected_campaigns=[],
        )

    try:
        targeting_result = targeting_client.evaluate(
            ad_request=request,
            candidates=active_campaigns,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "ADS Gateway could not evaluate targeting through "
                f"Targeting Service: {exc}"
            ),
        ) from exc

    if not targeting_result.eligible_campaigns:
        return AdDecisionResponse(
            request_id=trace.request_id,
            trace_id=trace.trace_id,
            decision_id=trace.decision_id,
            selected_campaign_id=None,
            selected_creative_id=None,
            status="NO_FILL_TARGETING",
            reason="No active campaigns passed targeting filters.",
            candidate_count=len(active_campaigns),
            candidate_campaign_ids=[
                campaign.campaign_id for campaign in active_campaigns
            ],
            eligible_candidate_count=0,
            eligible_campaign_ids=[],
            rejected_campaigns=targeting_result.rejected_campaigns,
        )

    selected_campaign = targeting_result.eligible_campaigns[0]

    return AdDecisionResponse(
        request_id=trace.request_id,
        trace_id=trace.trace_id,
        decision_id=trace.decision_id,
        selected_campaign_id=selected_campaign.campaign_id,
        selected_creative_id=selected_campaign.creative_id,
        status="TARGETING_DECISION_RETURNED",
        reason=(
            "Temporary selection made from campaigns that passed targeting. "
            "Ranking logic will be added in a later release."
        ),
        candidate_count=len(active_campaigns),
        candidate_campaign_ids=[
            campaign.campaign_id for campaign in active_campaigns
        ],
        eligible_candidate_count=len(targeting_result.eligible_campaigns),
        eligible_campaign_ids=[
            campaign.campaign_id
            for campaign in targeting_result.eligible_campaigns
        ],
        rejected_campaigns=targeting_result.rejected_campaigns,
    )