from cassandra.cluster import Cluster
import json, os

class CassandraDatabaseClient:

    def __init__(self):
        self.__connect()
    
    def __connect(self):
        config: dict = {}
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "cassandra.json")
        with open(file_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)

        cluster = Cluster(config.get("contact_points"))
        self.session = cluster.connect()

        self.session.set_keyspace(config.get("keyspace"))

    def select(self, table: str, where: str):
        if where:
            return self.session.execute(f"SELECT * FROM {table} WHERE {where}")
        else:
            return self.session.execute(f"SELECT * FROM {table} limit 20")
    
    def select_with_limit(self, column_names, table: str):
        return self.session.execute(f"SELECT {", ".join(column_names)} from {table}")
    
    def get_keyspaces(self):
        return self.session.execute("SELECT * FROM system_schema.keyspaces")
    
    def get_tables_info(self, keyspace: str):
        return self.session.execute(f"SELECT * FROM system_schema.tables WHERE keyspace_name = '{keyspace}';")

    def get_table_info(self, keyspace:str, table: str):
        return sorted(self.session.execute(f"SELECT * FROM system_schema.columns WHERE keyspace_name = '{keyspace}' AND table_name = '{table}';"), key=lambda x: (x.kind, x.column_name))
    