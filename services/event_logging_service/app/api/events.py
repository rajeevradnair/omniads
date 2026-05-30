from fastapi import APIRouter

from libs.contracts.events import EventIngestRequest, EventIngestResponse
from services.event_logging_service.app.logic.local_event_writer import (
    LocalEventWriter,
)

router = APIRouter()

_event_writer = LocalEventWriter()


@router.post("/api/v1/events", response_model=EventIngestResponse)
def ingest_event(request: EventIngestRequest) -> EventIngestResponse:
    """Ingest one ad event and write it to the local event lake."""

    storage_path = _event_writer.write_event(request.event)

    return EventIngestResponse(
        event_id=request.event.event_id,
        event_type=request.event.event_type,
        status="INGESTED",
        storage_path=storage_path,
    )