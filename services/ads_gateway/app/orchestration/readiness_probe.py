import httpx

from libs.contracts.service_status import DependencyStatus


def check_http_dependency(
    name: str,
    health_url: str,
    timeout_seconds: float = 1.0,
) -> DependencyStatus:
    """Check whether an HTTP dependency is reachable."""

    try:
        response = httpx.get(health_url, timeout=timeout_seconds)
        response.raise_for_status()

        return DependencyStatus(
            name=name,
            status="ready",
            detail=None,
        )
    except httpx.HTTPError as exc:
        return DependencyStatus(
            name=name,
            status="failed",
            detail=str(exc),
        )