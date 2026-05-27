from pydantic import BaseModel, Field


class DependencyStatus(BaseModel):
    """Status of one downstream dependency."""

    name: str
    status: str
    detail: str | None = None


class ReadinessResponse(BaseModel):
    """Readiness response for a service accounting for dowsntream dependencies."""

    service: str
    status: str
    dependencies: list[DependencyStatus] = Field(default_factory=list)