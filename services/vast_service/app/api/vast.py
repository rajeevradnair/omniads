from fastapi import APIRouter

from libs.contracts.vast import VastRenderRequest, VastRenderResponse
from libs.contracts.vast import VastPodRenderRequest, VastPodRenderResponse
from services.vast_service.app.logic.vast_renderer import render_vast_xml, render_vast_pod_xml

router = APIRouter()


@router.post("/api/v1/vast/render", response_model=VastRenderResponse)
def render_vast(request: VastRenderRequest) -> VastRenderResponse:
    """Render VAST XML for a selected creative."""

    vast_xml = render_vast_xml(request)

    return VastRenderResponse(
        request_id=request.request_id,
        trace_id=request.trace_id,
        decision_id=request.decision_id,
        creative_id=request.creative_id,
        vast_xml=vast_xml,
    )

@router.post("/api/v1/vast/render_pod", response_model=VastPodRenderResponse)
def render_vast_pod(request: VastPodRenderRequest) -> VastPodRenderResponse:
    """Render VAST XML for a multi-ad pod."""

    vast_xml = render_vast_pod_xml(request)

    total_duration = sum(
        ad.duration_seconds
        for ad in request.selected_ads
    )

    return VastPodRenderResponse(
        request_id=request.request_id,
        trace_id=request.trace_id,
        decision_id=request.decision_id,
        ad_count=len(request.selected_ads),
        total_duration_seconds=total_duration,
        vast_xml=vast_xml,
    )