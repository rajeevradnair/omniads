from fastapi import FastAPI

from services.frequency_cap_service.app.api.frequency_caps import (
    router as frequency_caps_router,
)
from services.frequency_cap_service.app.api.health import router as health_router

app = FastAPI(
    title="OmniAds Frequency Cap Service",
    description="Viewer frequency cap service for OTT ad decisioning",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(frequency_caps_router)