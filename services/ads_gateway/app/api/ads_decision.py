import httpx
import time

from libs.observability.logger import log_event

from fastapi import APIRouter, HTTPException

from libs.contracts.ad_request import AdDecisionRequest
from libs.contracts.ad_response import AdDecisionResponse
from libs.contracts.vast import VastRenderRequest

from services.ads_gateway.app.clients.campaign_client import CampaignServiceClient
from services.ads_gateway.app.clients.targeting_client import TargetingServiceClient
from services.ads_gateway.app.clients.vast_client import VastServiceClient
from services.ads_gateway.app.clients.candidate_client import CandidateServiceClient
from services.ads_gateway.app.clients.frequency_cap_client import FrequencyCapServiceClient


from services.ads_gateway.app.config import (
    get_campaign_service_url,
    get_candidate_service_url,
    get_targeting_service_url,
    get_frequency_cap_service_url,
    get_vast_service_url,
)
from services.ads_gateway.app.orchestration.trace_context import (
    create_decision_trace,
)

router = APIRouter()


@router.post("/api/v1/ads_gateway/ads/decision", response_model=AdDecisionResponse)
def create_ad_decision(request: AdDecisionRequest) -> AdDecisionResponse:
    """Create an ad decision using Campaign and Targeting services."""

    trace = create_decision_trace()

    workflow_start = time.perf_counter()

    log_event(
        service_name="ads-gateway",
        operation_name="ad_decision_started",
        status="started",
        trace_id=trace.trace_id,
        request_id=trace.request_id,
        decision_id=trace.decision_id,
        extra={
            "placement_id": request.placement_id,
            "viewer_id": request.viewer_id,
            "session_id": request.session_id,
            "content_id": request.content_id,
        },
    )

    # Clients to various microservices
    campaign_client = CampaignServiceClient(
        base_url=get_campaign_service_url(),
    )
    candidate_client = CandidateServiceClient(
        base_url=get_candidate_service_url(),
    )
    targeting_client = TargetingServiceClient(
        base_url=get_targeting_service_url(),
    )
    frequency_cap_client = FrequencyCapServiceClient(
        base_url=get_frequency_cap_service_url(),
    )
    vast_client = VastServiceClient(
        base_url=get_vast_service_url(),
    )

    campaign_lookup_start = time.perf_counter()
    try:
        active_campaigns = campaign_client.list_active_campaigns(
            placement_id=request.placement_id,
        )
        log_event(
            service_name="ads-gateway",
            operation_name="campaign_lookup",
            status="success",
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            decision_id=trace.decision_id,
            latency_ms=(time.perf_counter() - campaign_lookup_start) * 1000,
            extra={"candidate_count": len(active_campaigns)},
        )
    except httpx.HTTPError as exc:
        log_event(
            service_name="ads-gateway",
            operation_name="campaign_lookup",
            status="failed",
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            decision_id=trace.decision_id,
            error_type=type(exc).__name__,
        )

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

    candidate_lookup_start = time.perf_counter()
    try:
        candidate_result = candidate_client.generate(
            ad_request=request,
            active_campaigns=active_campaigns,
            max_candidates=3,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "ADS Gateway could not generate candidates through "
                f"Candidate Service: {exc}"
            ),
        ) from exc

    if not candidate_result.candidates:
        return AdDecisionResponse(
            request_id=trace.request_id,
            trace_id=trace.trace_id,
            decision_id=trace.decision_id,
            selected_campaign_id=None,
            selected_creative_id=None,
            status="NO_FILL_CANDIDATES",
            reason="Candidate Service returned no candidates.",
            candidate_count=len(active_campaigns),
            candidate_campaign_ids=[
                campaign.campaign_id for campaign in active_campaigns
            ],
            generated_candidate_count=0,
            generated_candidate_campaign_ids=[],
            candidate_reasons=[],
            eligible_candidate_count=0,
            eligible_campaign_ids=[],
            rejected_campaigns=[],
            vast_xml=None,
        )

    candidates = candidate_result.candidates

    targeting_lookup_start = time.perf_counter()
    try:
        targeting_result = targeting_client.evaluate(
            ad_request=request,
            candidates=candidates,
        )
        log_event(
            service_name="ads-gateway",
            operation_name="targeting_lookup",
            status="success",
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            decision_id=trace.decision_id,
            latency_ms=(time.perf_counter() - targeting_lookup_start) * 1000,
        )
    except httpx.HTTPError as exc:

        log_event(
            service_name="ads-gateway",
            operation_name="targeting_lookup",
            status="failed",
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            decision_id=trace.decision_id,
            error_type=type(exc).__name__,
        )

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

    try:
        frequency_cap_result = frequency_cap_client.evaluate(
            ad_request=request,
            candidates=targeting_result.eligible_campaigns,
            max_daily_impressions_per_creative=3,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "ADS Gateway could not evaluate frequency caps through "
                f"Frequency Cap Service: {exc}"
            ),
        ) from exc

    if not frequency_cap_result.allowed_candidates:
        return AdDecisionResponse(
            request_id=trace.request_id,
            trace_id=trace.trace_id,
            decision_id=trace.decision_id,
            selected_campaign_id=None,
            selected_creative_id=None,
            status="NO_FILL_FREQUENCY_CAP",
            reason="All eligible candidates were blocked by frequency caps.",
            candidate_count=len(active_campaigns),
            candidate_campaign_ids=[
                campaign.campaign_id for campaign in active_campaigns
            ],
            generated_candidate_count=len(candidate_result.candidates),
            generated_candidate_campaign_ids=[
                campaign.campaign_id for campaign in candidate_result.candidates
            ],
            candidate_reasons=candidate_result.candidate_reasons,
            eligible_candidate_count=len(targeting_result.eligible_campaigns),
            eligible_campaign_ids=[
                campaign.campaign_id
                for campaign in targeting_result.eligible_campaigns
            ],
            rejected_campaigns=targeting_result.rejected_campaigns,
            frequency_cap_allowed_count=0,
            frequency_cap_allowed_campaign_ids=[],
            frequency_cap_blocked=frequency_cap_result.blocked_candidates,
            frequency_cap_recorded_count=None,
            vast_xml=None,
        )
    
    selected_campaign = frequency_cap_result.allowed_candidates[0]

    vast_lookup_start = time.perf_counter()

    vast_request = VastRenderRequest(
        request_id=trace.request_id,
        trace_id=trace.trace_id,
        decision_id=trace.decision_id,
        campaign_id=selected_campaign.campaign_id,
        creative_id=selected_campaign.creative_id,
        creative_name=selected_campaign.creative_name,
        advertiser_name=selected_campaign.advertiser_name,
        media_url=selected_campaign.media_url,
        duration_seconds=selected_campaign.duration_seconds,
    )

    try:
        vast_response = vast_client.render_vast(vast_request)
    
        log_event(
            service_name="ads-gateway",
            operation_name="vast_lookup",
            status="success",
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            decision_id=trace.decision_id,
            latency_ms=(time.perf_counter() - vast_lookup_start) * 1000,
        )
    
    except httpx.HTTPError as exec:

        log_event(
            service_name="ads-gateway",
            operation_name="vast_lookup",
            status="failed",
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            decision_id=trace.decision_id,
            error_type=type(exc).__name__,
        )

        raise HTTPException(
            status_code=502,
            detail=f"ADS Gateway could not render VAST XML: {exec}",
        ) from exec

    try:
        cap_record_response = frequency_cap_client.record(
            viewer_id=request.viewer_id,
            campaign_id=selected_campaign.campaign_id,
            creative_id=selected_campaign.creative_id,
            decision_id=trace.decision_id,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "ADS Gateway could not record frequency cap exposure: "
                f"{exc}"
            ),
        ) from exc

    return AdDecisionResponse(
        request_id=trace.request_id,
        trace_id=trace.trace_id,
        decision_id=trace.decision_id,
        selected_campaign_id=selected_campaign.campaign_id,
        selected_creative_id=selected_campaign.creative_id,
        status="TARGETING_DECISION_RETURNED",
        reason=(
            "Temporary selection made from campaigns that passed top-K candidate retrieval & targeting. "
            "Ranking logic to be added in a later release."
        ),
        candidate_count=len(active_campaigns),
        candidate_campaign_ids=[
            campaign.campaign_id for campaign in active_campaigns
        ],
        generated_candidate_count=len(candidate_result.candidates),
        generated_candidate_campaign_ids=[
            campaign.campaign_id for campaign in candidate_result.candidates
        ],
        candidate_reasons=candidate_result.candidate_reasons,
        eligible_candidate_count=len(targeting_result.eligible_campaigns),
        eligible_campaign_ids=[
            campaign.campaign_id
            for campaign in targeting_result.eligible_campaigns
        ],
        rejected_campaigns=targeting_result.rejected_campaigns,
        vast_xml=vast_response.vast_xml,
        frequency_cap_allowed_count=len(frequency_cap_result.allowed_candidates),
        frequency_cap_allowed_campaign_ids=[
            campaign.campaign_id
            for campaign in frequency_cap_result.allowed_candidates
        ],
        frequency_cap_blocked=frequency_cap_result.blocked_candidates,
        frequency_cap_recorded_count=cap_record_response.new_count,
    )