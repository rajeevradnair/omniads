from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/vast/health")
def health_check() -> dict:
    """Return VAST Service health status."""

    return {
        "service": "vast-service",
        "status": "healthy",
    }