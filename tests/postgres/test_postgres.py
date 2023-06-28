from pipeline.config.connections import get_postgres_connection_credentials
from pipeline.utils.postgres import database_connection
from pipeline.clients.database import PostgresClient

import pytest


@pytest.fixture()
def setup(postgres_credentials):
    with database_connection(get_postgres_connection_credentials()) as connection:

        connection.execute(f"""truncate table production.trades;""")
        connection.execute("""
            INSERT INTO production.trades (id, ticker, price, quantity, status, source)
            VALUES 
                (1, 'TSLA', 100.00, 10, 'OPEN', '2023-06-23-trades-1'),
                (2, 'TSLA', 100.00, 10, 'OPEN', '2023-06-23-trades-2'),
                (1, 'TSLA', 100.00, 10, 'CLOSED', '2023-06-24-trades-1')
            ;""")
    yield


def test_postgres_client_get_distinct_sources(setup, postgres_credentials):

    with database_connection(get_postgres_connection_credentials()) as connection:

        client = PostgresClient(connection=connection)
        result = client.get_distinct_sources(schema='production', table_name='trades')

        assert result == {'2023-06-23-trades-1', '2023-06-24-trades-1', '2023-06-23-trades-2'}    

def test_postgres_client_delete_sources(setup, postgres_credentials):

    with database_connection(get_postgres_connection_credentials()) as connection:
        
        client = PostgresClient(connection=connection)
        client.delete_sources(schema='production', table_name='trades', sources=['2023-06-24-trades-1'])

        connection.execute(f"""select distinct source from production.trades;""")
        result = sorted(set([source[0] for source in connection.fetchall()]))

        assert result == ['2023-06-23-trades-1', '2023-06-23-trades-2']

