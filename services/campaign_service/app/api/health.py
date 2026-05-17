from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/campaigns/health")
def health_check() -> dict:
    return {
        "service": "campaign-service",
        "status": "healthy",
    }