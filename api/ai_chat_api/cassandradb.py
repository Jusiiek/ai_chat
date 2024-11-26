from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from ai_chat_api.config import Config


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
            [Config.CASSANDRA_HOST],
            port=Config.CASSANDRA_PORT,
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
