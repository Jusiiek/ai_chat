from typing import Type, List

from cassandra.cluster import Cluster, DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.management import (
    sync_table,
    drop_table
)
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection

from ai_chat_api.config import Config
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.models.blacklisted_token import BlacklistedToken
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.models.task import Task


class DatabaseManager:
    _instance = None

    KEYSPACE = Config.APP_KEYSPACE
    MODELS: List[Type[Model]] = [
        User,
        Token,
        BlacklistedToken,
        Thread,
        Chat,
        Task
    ]

    def __init__(self):
        self.cluster = None
        self.session = None

    @classmethod
    def get_instance(cls) -> 'DatabaseManager':
        """
        Returns DatabaseManager instance
        """
        if not cls._instance:
            cls._instance = DatabaseManager()
        return cls._instance

    def _get_auth_provider(self):
        """
        Returns auth provider instance
        """
        return PlainTextAuthProvider(
            username=Config.CASSANDRA_USERNAME,
            password=Config.CASSANDRA_PASSWORD
        )

    def connect(self):
        """
        Creates connection to cassandra and returns
        connection object (session)
        """
        try:
            self.cluster = Cluster(
                [Config.CASSANDRA_HOST],
                port=Config.CASSANDRA_PORT,
                auth_provider=self._get_auth_provider(),
                protocol_version=5,
                load_balancing_policy=DCAwareRoundRobinPolicy(local_dc="datacenter1")
            )

            self.session = self.cluster.connect()
            self._create_keyspace()
            self.session.set_keyspace(self.KEYSPACE)

            connection.register_connection(
                "default",
                hosts=[Config.CASSANDRA_HOST]
            )
            connection.set_default_connection("default")

            return self.session
        except Exception as e:
            print(f"Failed to connect to Cassandra cluster: {str(e)}")
            raise

    def close(self):
        """
        Closes connection to cassandra
        """
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
        print("Cassandra connection closed.")

    def _create_keyspace(self):
        if self.session:
            self.session.execute("""
                    CREATE KEYSPACE IF NOT EXISTS {}
                    WITH replication = {{
                    'class': 'SimpleStrategy', 'replication_factor': '1'
                    }}
                """.format(self.KEYSPACE))

            self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS {}
                WITH replication = {{
                'class': 'SimpleStrategy', 'replication_factor': '1'
                }}""".format("celeryks"))

    def _delete_keyspace(self):
        if self.session:
            self.session.execute(
                f"DROP KEYSPACE IF EXISTS {self.KEYSPACE}"
            )

    def drop_db(self):
        """
        Drops models tables
        """
        for model in self.MODELS:
            try:
                drop_table(model)
                print(f"Successfully dropped table for model: {model.__name__}")
            except Exception as e:
                print(f"Failed to drop table for model {model.__name__}: {e}")

    def create_db(self):
        """
        Creates models tables
        """
        for model in self.MODELS:
            try:
                sync_table(model)
                print(f"Successfully created table for model: {model.__name__}")
            except Exception as e:
                print(f"Failed to create table for model: {model.__name__}: {e}")
