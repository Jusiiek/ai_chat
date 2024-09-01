from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from ai_chat_api.config import Config


class CassandraNodes:
    CASSANDRA_1 = {
        "host": "0.0.0.0",
        "port": 9042
    }
    CASSANDRA_2 = {
        "host": "0.0.0.0",
        "port": 9043
    }
    CASSANDRA_3 = {
        "host": "0.0.0.0",
        "port": 9044
    }

    @staticmethod
    def get_cassandra_nodes():
        """
        Returns all nodes available in cassandra.

        return
        --------------
        nodes: list - list of cassandra nodes
        """
        nodes = [
            CassandraNodes.CASSANDRA_1,
            CassandraNodes.CASSANDRA_2,
            CassandraNodes.CASSANDRA_3,
        ]

        return nodes


class CassandraConnection:
    def __init__(self):
        self.cluster = None
        self.session = None

    def _get_auth_provider(self):
        """
        Returns auth provider instance
        """
        return PlainTextAuthProvider(
            username=Config.CASSANDRA_USERNAME,
            password=Config.CASSANDRA_PASSWORD
        )

    def create_cassandra_connection(self):
        """
        Creates connection to cassandra and returns
        connection object (session)
        """
        self.cluster = Cluster(
            [
                (node["host"], node["port"])
                for node in CassandraNodes.get_cassandra_nodes()
            ],
            auth_provider=self._get_auth_provider(),
        )

        self.session = self.cluster.connect()
        return self.session

    def close_connection(self):
        """
        Closes connection to cassandra
        """
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
        print("Cassandra connection closed.")
