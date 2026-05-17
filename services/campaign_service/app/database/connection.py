from collections.abc import Iterator

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row

from services.campaign_service.app.config import get_database_url


def get_connection() -> Iterator[Connection]:
    """Yield a PostgreSQL connection.

    This function is used as a FastAPI dependency. It opens a connection for
    the request and closes it after the request finishes.
    """

    connection = psycopg.connect(
        get_database_url(),
        row_factory=dict_row,
    )

    try:
        yield connection
    finally:
        connection.close()