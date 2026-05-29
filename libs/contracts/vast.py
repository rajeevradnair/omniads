from pydantic import BaseModel
from libs.contracts.ranking import RankedCandidate

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

class VastPodRenderRequest(BaseModel):
    """Request to render VAST XML for a packed ad pod."""

    request_id: str
    trace_id: str
    decision_id: str
    selected_ads: list[RankedCandidate]


class VastPodRenderResponse(BaseModel):
    """Response after rendering VAST XML for a packed ad pod."""

    request_id: str
    trace_id: str
    decision_id: str
    ad_count: int
    total_duration_seconds: int
    vast_xml: str