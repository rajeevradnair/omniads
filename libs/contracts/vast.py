from pydantic import BaseModel


class VastRenderRequest(BaseModel):
    """Request sent to VAST Service to render VAST XML."""

    request_id: str
    trace_id: str
    decision_id: str
    campaign_id: str
    creative_id: str
    creative_name: str
    advertiser_name: str
    media_url: str
    duration_seconds: int


class VastRenderResponse(BaseModel):
    """Response returned by VAST Service."""

    request_id: str
    trace_id: str
    decision_id: str
    creative_id: str
    vast_xml: str