from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/frequency_caps/health")
def health_check() -> dict:
    """Return Frequency Cap Service health status."""

    return {
        "service": "frequency-cap-service",
        "status": "healthy",
    }