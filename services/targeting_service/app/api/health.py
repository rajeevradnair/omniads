from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/targeting/health")
def health_check() -> dict:
    return {
        "service": "targeting-service",
        "status": "healthy",
    } 
