from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AdEventType(str, Enum):
    """Supported OmniAds event types."""

    AD_DECISION_CREATED = "AD_DECISION_CREATED"
    VAST_RETURNED = "VAST_RETURNED"
    IMPRESSION_RECEIVED = "IMPRESSION_RECEIVED"
    CLICK_RECEIVED = "CLICK_RECEIVED"
    CONVERSION_RECEIVED = "CONVERSION_RECEIVED"
    NO_FILL_RETURNED = "NO_FILL_RETURNED"


class AdEvent(BaseModel):
    """Canonical event emitted by OmniAds services."""

    event_id: str = Field(default_factory=lambda: f"evt_{uuid4().hex}")
    event_type: AdEventType
    event_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    request_id: str
    trace_id: str
    decision_id: str

    viewer_id: str | None = None
    session_id: str | None = None
    content_id: str | None = None
    placement_id: str | None = None
    ad_break_id: str | None = None

    campaign_id: str | None = None
    creative_id: str | None = None

    device: str | None = None
    geo: str | None = None

    status: str | None = None
    event_source: str = "ads-gateway"

    attributes: dict[str, Any] = Field(default_factory=dict)


class EventIngestRequest(BaseModel):
    """Request sent to Event Logging Service."""

    event: AdEvent


class EventIngestResponse(BaseModel):
    """Acknowledgement returned after event ingestion."""

    event_id: str
    event_type: AdEventType
    status: str
    storage_path: str | None = None