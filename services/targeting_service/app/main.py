from fastapi import FastAPI

from services.targeting_service.app.api.health import router as health_router
from services.targeting_service.app.api.targeting import router as targeting_router


app = FastAPI(
    title="OmniAds Targeting Service",
    description="Eligibility and targeting service for OTT ad decisioning",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(targeting_router)
