import json
from pathlib import Path

from libs.contracts.events import AdEvent


class LocalEventWriter:
    """Writes ad events to local partitioned JSONL files."""

    def __init__(self, base_path: str = "data/synthetic_events"):
        self._base_path = Path(base_path)

    def write_event(self, event: AdEvent) -> str:
        """Write an event to a partitioned JSONL file and return its path."""

        event_type_partition = event.event_type.value.lower()
        event_date = event.event_timestamp.date().isoformat()
        event_timestamp = event.event_timestamp

        partition_path = (
            self._base_path
            / f"event_type={event_type_partition}"
            / f"year={event_timestamp.year:04d}"
            / f"month={event_timestamp.month:02d}"
            / f"day={event_timestamp.day:02d}"
        )
        partition_path.mkdir(parents=True, exist_ok=True)

        file_path = partition_path / "events.jsonl"

        with file_path.open("a", encoding="utf-8") as file:
            file.write(event.model_dump_json() + "\n")

        return str(file_path)