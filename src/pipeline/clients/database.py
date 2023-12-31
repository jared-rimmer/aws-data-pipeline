from pipeline.connections.postgres import database_connection


class PostgresClient:
    def __init__(self, connection: database_connection):
        self.cursor = connection

    def get_distinct_sources(self, schema: str, table_name: str) -> set:
        result = self.cursor.run(
            f"""select distinct source_file_name from {schema}.{table_name};"""
        )

        return set([source[0] for source in result])

    def delete_sources(self, schema: str, table_name: str, sources: list) -> set:
        edit = (",").join([f"'{source}'" for source in sources])

        self.cursor.run(
            f"""delete from {schema}.{table_name} where source_file_name in ({edit});"""
        )
