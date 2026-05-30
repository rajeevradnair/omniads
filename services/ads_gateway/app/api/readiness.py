from fastapi import APIRouter

from libs.contracts.service_status import ReadinessResponse
from services.ads_gateway.app.config import (
    get_campaign_service_url,
    get_candidate_service_url,
    get_targeting_service_url,
    get_frequency_cap_service_url,
    get_budget_pacing_service_url,
    get_ranking_service_url,
    get_vast_service_url,
    get_event_logging_service_url,
)
from services.ads_gateway.app.orchestration.readiness_probe import (
    check_http_dependency,
)

router = APIRouter()


@router.get("/api/v1/ads_gateway/readiness", response_model=ReadinessResponse)
def readiness_check() -> ReadinessResponse:
    """Return ADS Gateway readiness status."""

    dependencies = [
        check_http_dependency(
            name="campaign-service",
            health_url=f"{get_campaign_service_url()}/api/v1/campaigns/health",
        ),
        check_http_dependency(
            name="candidate-service",
            health_url=f"{get_candidate_service_url()}/api/v1/candidates/health",
        ),
        check_http_dependency(
            name="targeting-service",
            health_url=f"{get_targeting_service_url()}/api/v1/targeting/health",
        ),
        check_http_dependency(
            name="frequency-cap-service",
            health_url=f"{get_frequency_cap_service_url()}/api/v1/frequency_caps/health",
        ),
        check_http_dependency(
            name="budget-pacing-service",
            health_url=f"{get_budget_pacing_service_url()}/api/v1/pacing/health",
        ),
        check_http_dependency(
            name="ranking-service",
            health_url=f"{get_ranking_service_url()}/api/v1/ranking/health",
        ),
        check_http_dependency(
            name="vast-service",
            health_url=f"{get_vast_service_url()}/api/v1/vast/health",
        ),
        check_http_dependency(
            name="event-logging-service",
            health_url=f"{get_event_logging_service_url()}/api/v1/events/health",
        ),
    ]

    is_ready = all(
        dependency.status == "ready"
        for dependency in dependencies
    )

    return ReadinessResponse(
        service="ads-gateway",
        status="ready" if is_ready else "not_ready",
        dependencies=dependencies,
    )