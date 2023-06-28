from pipeline.utils.postgres import database_connection


class PostgresClient:

    def __init__(self, connection: database_connection):
        self.cursor = connection

    def get_distinct_sources(self, schema: str, table_name: str) -> set:
        self.cursor.execute(f"""select distinct source from {schema}.{table_name};""")
        
        return set([source[0] for source in self.cursor.fetchall()])

    def delete_sources(self, schema: str, table_name: str, sources: list) -> set:

        edit = (',').join([f"'{source}'" for source in sources])

        self.cursor.execute(f"""delete from {schema}.{table_name} where source in ({edit});""")
        