from psycopg import Connection

from libs.contracts.campaign import ActiveCampaign


class CampaignRepository:
    """Database access layer for campaign data."""

    def __init__(self, connection: Connection):
        self._connection = connection

    def list_active_campaigns(self, placement_id: str) -> list[ActiveCampaign]:
        """Return active campaigns eligible for a placement.

        Args:
            placement_id: Placement where the ad should be shown.

        Returns:
            A list of active campaign + creative records.
        """

        query = """
            SELECT
                c.campaign_id,
                c.campaign_name,
                c.advertiser_id,
                a.advertiser_name,
                c.objective,
                c.daily_budget_usd,
                c.base_bid_cpm_usd,
                cr.creative_id,
                cr.creative_name,
                cr.media_url,
                cr.duration_seconds,
                cp.placement_id
            FROM campaigns c
            JOIN advertisers a
                ON c.advertiser_id = a.advertiser_id
            JOIN creatives cr
                ON c.campaign_id = cr.campaign_id
            JOIN campaign_placements cp
                ON c.campaign_id = cp.campaign_id
            WHERE c.status = 'ACTIVE'
              AND cr.status = 'ACTIVE'
              AND cp.placement_id = %s
              AND NOW() BETWEEN c.starts_at AND c.ends_at
            ORDER BY c.base_bid_cpm_usd DESC;
        """

        with self._connection.cursor() as cursor:
            cursor.execute(query, (placement_id,))
            rows = cursor.fetchall()

        return [ActiveCampaign(**row) for row in rows]