from fastapi import FastAPI

from services.budget_pacing_service.app.api.health import router as health_router
from services.budget_pacing_service.app.api.pacing import router as pacing_router

app = FastAPI(
    title="OmniAds Budget Pacing Service",
    description="Campaign budget pacing service for OTT ad decisioning",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(pacing_router)