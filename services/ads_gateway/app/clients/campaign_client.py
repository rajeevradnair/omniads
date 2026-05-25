import httpx

from libs.contracts.campaign import ActiveCampaign

class CampaignServiceClient:
    def __init__(self, base_url: str, timeout_seconds:float = 2.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def list_active_campaigns(self, placement_id: str) -> list[ActiveCampaign]:
        url = self.base_url + "/api/v1/campaigns/active"
        response = httpx.get(
            url, 
            params={"placement_id": placement_id}, 
            timeout=self.timeout_seconds
        )
        response.raise_for_status()
        response_payload = response.json()

        return [ActiveCampaign(**campaign) for campaign in response_payload]
