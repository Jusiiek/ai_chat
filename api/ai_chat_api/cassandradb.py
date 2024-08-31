from enum import Enum

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

from ai_chat_api.config import Config


class CassandraNodes(Enum):
    CASSANDRA_1 = "cassandra1"
    CASSANDRA_2 = "cassandra2"
    CASSANDRA_3 = "cassandra3"


class CassandraConnection:
    def _get_auth_provider(self):
        return PlainTextAuthProvider(
            username=Config.CASSANDRA_USERNAME,
            password=Config.CASSANDRA_PASSWORD
        )

    def create_cassandra_connection(self):

        cluster = Cluster(
            [cluster.value for cluster in CassandraNodes],
            auth_provider=self._get_auth_provider(),
        )

        session = cluster.connect()
        connection.set_session(session)
        return session
