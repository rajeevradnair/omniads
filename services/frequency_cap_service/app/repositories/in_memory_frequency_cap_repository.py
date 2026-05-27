from datetime import datetime, timezone


class InMemoryFrequencyCapRepository:
    """In-memory repository that simulates DynamoDB frequency counters.

    This is for local development only. The same interface can later be
    implemented using DynamoDB atomic counters and TTL.
    """

    def __init__(self):
        self._counts: dict[str, int] = {}

    def get_count(self, viewer_id: str, creative_id: str) -> int:
        """Return current daily impression count for viewer + creative."""

        key = self._build_daily_key(
            viewer_id=viewer_id,
            creative_id=creative_id,
        )
        return self._counts.get(key, 0)

    def increment_count(self, viewer_id: str, creative_id: str) -> int:
        """Increment and return daily impression count for viewer + creative."""

        key = self._build_daily_key(
            viewer_id=viewer_id,
            creative_id=creative_id,
        )
        current_count = self._counts.get(key, 0)
        new_count = current_count + 1
        self._counts[key] = new_count
        return new_count

    def _build_daily_key(self, viewer_id: str, creative_id: str) -> str:
        """Build a DynamoDB-style daily counter key."""

        current_date = datetime.now(timezone.utc).date().isoformat()
        return f"VIEWER#{viewer_id}#CREATIVE#{creative_id}#DAY#{current_date}"