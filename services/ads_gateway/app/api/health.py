from fastapi import APIRouter

router = APIRouter()

@router.get("/services/ads_gateway/app/api/health")
def health_check() -> dict:
    return {
        "service": "ads_gateway",
        "status": "healthy",
    }