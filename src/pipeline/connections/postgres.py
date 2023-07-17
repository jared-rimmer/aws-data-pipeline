from contextlib import contextmanager
from dataclasses import asdict

import pg8000.native

from pipeline.config.connections import PostgresConnectionConfig


@contextmanager
def database_connection(postgres_connection_config: PostgresConnectionConfig):
    connection = pg8000.native.Connection(**asdict(postgres_connection_config))

    try:
        yield connection
    finally:
        connection.close()
