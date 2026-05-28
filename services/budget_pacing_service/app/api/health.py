from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/pacing/health")
def health_check() -> dict:
    """Return Budget Pacing Service health status."""

    return {
        "service": "budget-pacing-service",
        "status": "healthy",
    }