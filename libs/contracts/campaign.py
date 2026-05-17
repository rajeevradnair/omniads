from pydantic import BaseModel


class ActiveCampaign(BaseModel):
    """Campaign and creative data eligible for a placement."""

    campaign_id: str
    campaign_name: str
    advertiser_id: str
    advertiser_name: str
    objective: str
    daily_budget_usd: float
    base_bid_cpm_usd: float
    # Status not being returned as class itself is "ActiveCampaign"
    # Temporarily involving creative information. May refactor later
    creative_id: str
    creative_name: str
    media_url: str
    duration_seconds: int
    placement_id: str