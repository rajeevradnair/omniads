from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/events/health")
def health_check() -> dict:
    """Return Event Logging Service health status."""

    return {
        "service": "event-logging-service",
        "status": "healthy",
    }