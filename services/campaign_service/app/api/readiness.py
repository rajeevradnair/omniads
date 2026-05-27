from fastapi import APIRouter

from libs.contracts.service_status import DependencyStatus, ReadinessResponse
from services.campaign_service.app.database.connection import (
    can_connect_to_database,
)

router = APIRouter()


@router.get("/api/v1/campaigns/readiness", response_model=ReadinessResponse)
def readiness_check() -> ReadinessResponse:
    """Return Campaign Service readiness status."""

    database_ready, detail = can_connect_to_database()

    dependency = DependencyStatus(
        name="postgres",
        status="ready" if database_ready else "failed",
        detail=detail,
    )

    return ReadinessResponse(
        service="campaign-service",
        status="ready" if database_ready else "not_ready",
        dependencies=[dependency],
    )