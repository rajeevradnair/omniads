from fastapi import FastAPI

from services.candidate_service.app.api.candidates import (
    router as candidates_router,
)
from services.candidate_service.app.api.health import router as health_router

app = FastAPI(
    title="OmniAds Candidate Service",
    description="Candidate generation service for OTT ad decisioning",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(candidates_router)