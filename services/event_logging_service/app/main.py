from fastapi import FastAPI

from services.event_logging_service.app.api.events import router as events_router
from services.event_logging_service.app.api.health import router as health_router

app = FastAPI(
    title="OmniAds Event Logging Service",
    description="Event ingestion service for ad decision analytics",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(events_router)