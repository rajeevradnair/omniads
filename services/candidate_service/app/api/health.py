from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/candidates/health")
def health_check() -> dict:
    """Return Candidate Service health status."""

    return {
        "service": "candidate-service",
        "status": "healthy",
    }