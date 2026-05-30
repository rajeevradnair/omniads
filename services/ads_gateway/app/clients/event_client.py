import httpx

from libs.contracts.events import AdEvent, EventIngestRequest, EventIngestResponse


class EventLoggingServiceClient:
    """HTTP client for sending events to Event Logging Service."""

    def __init__(self, base_url: str, timeout_seconds: float = 2.0):
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def ingest(self, event: AdEvent) -> EventIngestResponse:
        """Send one event to the Event Logging Service."""

        url = f"{self._base_url}/api/v1/events"

        payload = EventIngestRequest(event=event)

        response = httpx.post(
            url,
            json=payload.model_dump(mode="json"),
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()

        return EventIngestResponse(**response.json())