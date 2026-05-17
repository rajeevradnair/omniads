from fastapi import APIRouter, Depends, Query
from psycopg import Connection

from libs.contracts.campaign import ActiveCampaign
from services.campaign_service.app.database.connection import get_connection
from services.campaign_service.app.repositories.campaign_repository import (
    CampaignRepository,
)

router = APIRouter()


@router.get("/api/v1/campaigns/active", response_model=list[ActiveCampaign])
def list_active_campaigns(
    placement_id: str = Query(..., description="Placement identifier"),
    connection: Connection = Depends(get_connection),
) -> list[ActiveCampaign]:
    """Return active campaigns for a placement."""

    repository = CampaignRepository(connection)
    return repository.list_active_campaigns(placement_id)