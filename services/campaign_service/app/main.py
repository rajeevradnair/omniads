from fastapi import FastAPI

from services.campaign_service.app.api.health import router as health_router
from services.campaign_service.app.api.campaigns import ( router as campaigns_router,)
from services.campaign_service.app.api.readiness import router as readiness_router

app = FastAPI(
    title="OmniAds Campaign Service",
    description="Campaign metadata service for OTT ad decisioning",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(campaigns_router)
app.include_router(readiness_router)