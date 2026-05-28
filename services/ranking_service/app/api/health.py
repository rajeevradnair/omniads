from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/ranking/health")
def health_check() -> dict:
    """Return Ranking Service health status."""

    return {
        "service": "ranking-service",
        "status": "healthy",
    }