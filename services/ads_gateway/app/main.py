from fastapi import FastAPI
from services.ads_gateway.app.api.health import router as health_router
from services.ads_gateway.app.api.ads_decision import router as ads_decision_router
from services.ads_gateway.app.api.readiness import router as readiness_router
from services.ads_gateway.app.api.events import router as events_router

app = FastAPI(
    title="OmniAds ADS Gateway",
    summary="Gateway service for OTT Ads-decision platform",
    version="0.1.0",
    description="0.1.0"
)

app.include_router(health_router)
app.include_router(ads_decision_router)
app.include_router(readiness_router)
app.include_router(events_router)