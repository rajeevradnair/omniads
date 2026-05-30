from pathlib import Path

import duckdb


EVENT_GLOB = (
    "data/synthetic_events/"
    "event_type=*/year=*/month=*/day=*/events.jsonl"
)


def main() -> None:
    """Run local analytics queries over partitioned event JSONL files."""

    if not _has_event_files():
        raise RuntimeError(
            "No event files found. Run the ad decision flow first."
        )

    connection = duckdb.connect(database=":memory:")

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW omniads_events AS
        SELECT *
        FROM read_json_auto(
            '{EVENT_GLOB}',
            hive_partitioning = true
        );
        """
    )

    print("\nEvent counts by type:")
    print(
        connection.execute(
            """
            SELECT
                event_type,
                COUNT(*) AS event_count
            FROM omniads_events
            GROUP BY event_type
            ORDER BY event_count DESC;
            """
        ).fetchdf()
    )

    print("\nEvent counts by partition date:")
    print(
        connection.execute(
            """
            SELECT
                year,
                month,
                day,
                event_type,
                COUNT(*) AS event_count
            FROM omniads_events
            GROUP BY year, month, day, event_type
            ORDER BY year, month, day, event_type;
            """
        ).fetchdf()
    )

    print("\nDecision to VAST completeness:")
    print(
        connection.execute(
            """
            SELECT
                decision_id,
                SUM(CASE WHEN event_type = 'ad_decision_created' THEN 1 ELSE 0 END)
                    AS decision_events,
                SUM(CASE WHEN event_type = 'vast_returned' THEN 1 ELSE 0 END)
                    AS vast_events
            FROM omniads_events
            GROUP BY decision_id
            ORDER BY decision_id;
            """
        ).fetchdf()
    )


def _has_event_files() -> bool:
    """Return whether the local event lake contains JSONL files."""

    return bool(
        list(
            Path("data/synthetic_events").glob(
                "event_type=*/year=*/month=*/day=*/events.jsonl"
            )
        )
    )


if __name__ == "__main__":
    main()