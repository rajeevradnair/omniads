import os


def get_database_url() -> str:
    """Return the PostgreSQL database connection URL."""

    return os.getenv(
        "DATABASE_URL",
        "postgresql://omniads:omniads@postgres:5432/omniads",
    )