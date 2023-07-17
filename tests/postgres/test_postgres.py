from pipeline.config.connections import get_postgres_connection_credentials
from pipeline.connections.postgres import database_connection
from pipeline.clients.database import PostgresClient

import pytest


@pytest.fixture()
def setup():
    with database_connection(get_postgres_connection_credentials()) as connection:
        connection.run(f"""truncate table production.trades;""")
        connection.run(
            """
            INSERT INTO production.trades (id, ticker, price, quantity, status, source_file_name)
            VALUES 
                (1, 'TSLA', 100.00, 10, 'OPEN', '2023-06-23-trades-1'),
                (2, 'TSLA', 100.00, 10, 'OPEN', '2023-06-23-trades-2'),
                (1, 'TSLA', 100.00, 10, 'CLOSED', '2023-06-24-trades-1')
            ;"""
        )
    yield


def test_postgres_client_get_distinct_sources(setup):
    with database_connection(get_postgres_connection_credentials()) as connection:
        client = PostgresClient(connection=connection)
        result = client.get_distinct_sources(schema="production", table_name="trades")

        assert result == {
            "2023-06-23-trades-1",
            "2023-06-24-trades-1",
            "2023-06-23-trades-2",
        }


def test_postgres_client_delete_sources(setup):
    with database_connection(get_postgres_connection_credentials()) as connection:
        client = PostgresClient(connection=connection)
        client.delete_sources(
            schema="production", table_name="trades", sources=["2023-06-24-trades-1"]
        )

        test = sorted(
            set(
                row[0]
                for row in connection.run(
                    f"""select distinct source_file_name from production.trades;"""
                )
            )
        )

        # result = sorted(set([source[0] for source in connection.fetchall()]))

        assert test == ["2023-06-23-trades-1", "2023-06-23-trades-2"]
