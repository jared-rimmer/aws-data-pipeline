from contextlib import contextmanager
from dataclasses import asdict

import psycopg2

from pipeline.config.connections import PostgresConnectionConfig

@contextmanager
def database_connection(postgres_connection_config: PostgresConnectionConfig):
    
    database_connection = psycopg2.connect(**asdict(postgres_connection_config))
    database_connection.autocommit = True

    try:
        cursor = database_connection.cursor()
        yield cursor
    finally:
        cursor.close()
        database_connection.close()
