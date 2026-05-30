from fastapi import APIRouter, Query

from libs.contracts.events import AdEvent, AdEventType
from services.ads_gateway.app.clients.event_client import EventLoggingServiceClient
from services.ads_gateway.app.config import get_event_logging_service_url

router = APIRouter()


@router.get("/api/v1/events/impression")
def record_impression(
    request_id: str = Query(...),
    trace_id: str = Query(...),
    decision_id: str = Query(...),
    campaign_id: str = Query(...),
    creative_id: str = Query(...),
) -> dict:
    """Record an impression tracking event."""

    event_client = EventLoggingServiceClient(
        base_url=get_event_logging_service_url(),
    )

    event = AdEvent(
        event_type=AdEventType.IMPRESSION_RECEIVED,
        request_id=request_id,
        trace_id=trace_id,
        decision_id=decision_id,
        campaign_id=campaign_id,
        creative_id=creative_id,
        status="IMPRESSION_RECEIVED",
        event_source="tracking-endpoint",
    )

    response = event_client.ingest(event)

    return {
        "status": "ok",
        "event_id": response.event_id,
    }


@router.get("/api/v1/events/click")
def record_click(
    request_id: str = Query(...),
    trace_id: str = Query(...),
    decision_id: str = Query(...),
    campaign_id: str = Query(...),
    creative_id: str = Query(...),
) -> dict:
    """Record a click tracking event."""

    event_client = EventLoggingServiceClient(
        base_url=get_event_logging_service_url(),
    )

    event = AdEvent(
        event_type=AdEventType.CLICK_RECEIVED,
        request_id=request_id,
        trace_id=trace_id,
        decision_id=decision_id,
        campaign_id=campaign_id,
        creative_id=creative_id,
        status="CLICK_RECEIVED",
        event_source="tracking-endpoint",
    )

    response = event_client.ingest(event)

    return {
        "status": "ok",
        "event_id": response.event_id,
    }