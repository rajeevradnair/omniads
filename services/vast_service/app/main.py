from fastapi import FastAPI

from services.vast_service.app.api.health import router as health_router
from services.vast_service.app.api.vast import router as vast_router

app = FastAPI(
    title="OmniAds VAST Service",
    description="MediaTailor-compatible VAST rendering service",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(vast_router)