from fastapi import APIRouter

from libs.contracts.vast import VastRenderRequest, VastRenderResponse
from services.vast_service.app.logic.vast_renderer import render_vast_xml

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