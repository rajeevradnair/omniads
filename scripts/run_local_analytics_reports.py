from pathlib import Path

import duckdb


EVENT_GLOB = (
    "data/synthetic_events/"
    "event_type=*/year=*/month=*/day=*/events.jsonl"
)

REPORT_SQL_FILES = [
    "sql/local/fill_rate.sql",
    "sql/local/campaign_performance.sql",
    "sql/local/creative_performance.sql",
    "sql/local/no_fill_reasons.sql",
    "sql/local/pacing_health.sql",
]


def main() -> None:
    """Run local analytics reports against the OmniAds event lake."""

    if not _has_event_files():
        raise RuntimeError(
            "No event files found under data/synthetic_events. "
            "Run the ad decision flow first so events are generated."
        )

    connection = duckdb.connect(database=":memory:")

    _create_events_view(connection)

    for sql_file in REPORT_SQL_FILES:
        _run_report(connection, sql_file)


def _create_events_view(connection: duckdb.DuckDBPyConnection) -> None:
    """Create an in-memory SQL view over partitioned JSONL event files."""

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


def _run_report(connection: duckdb.DuckDBPyConnection, sql_file: str) -> None:
    """Run one SQL report file and print its result."""

    sql_path = Path(sql_file)

    if not sql_path.exists():
        print(f"\nSKIP: {sql_file} does not exist yet.")
        return

    query = sql_path.read_text(encoding="utf-8")

    print("\n" + "=" * 80)
    print(f"REPORT: {sql_file}")
    print("=" * 80)

    # Execute the queries in the sql file
    result = connection.execute(query).fetchdf()

    if result.empty:
        print("No rows returned.")
    else:
        print(result.to_string(index=False))


def _has_event_files() -> bool:
    """Return whether local event lake files exist."""

    return bool(
        list(
            Path("data/synthetic_events").glob(
                "event_type=*/year=*/month=*/day=*/events.jsonl"
            )
        )
    )


if __name__ == "__main__":
    main()