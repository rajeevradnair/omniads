from datetime import datetime, timezone


class InMemoryBudgetRepository:
    """In-memory repository that simulates DynamoDB campaign spend state."""

    def __init__(self):
        self._spend_by_key: dict[str, float] = {}

    def get_spend(self, campaign_id: str) -> float:
        """Return current daily spend for a campaign."""

        key = self._build_daily_key(campaign_id)
        return self._spend_by_key.get(key, 0.0)

    def increment_spend(self, campaign_id: str, spend_usd: float) -> float:
        """Increment and return daily campaign spend."""

        key = self._build_daily_key(campaign_id)
        current_spend = self._spend_by_key.get(key, 0.0)
        new_spend = current_spend + spend_usd
        self._spend_by_key[key] = new_spend
        return new_spend

    def _build_daily_key(self, campaign_id: str) -> str:
        """Build a DynamoDB-style daily campaign spend key."""

        current_date = datetime.now(timezone.utc).date().isoformat()
        return f"CAMPAIGN#{campaign_id}#DAY#{current_date}"
    
    def print(self) -> None:
        print(self._spend_by_key)