from fastapi import FastAPI

from services.ranking_service.app.api.health import router as health_router
from services.ranking_service.app.api.rank import router as rank_router

app = FastAPI(
    title="OmniAds Ranking Service",
    description="Auction ranking service for OTT ad decisioning",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(rank_router)