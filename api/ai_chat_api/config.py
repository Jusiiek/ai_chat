import os


class Config:
    """
    A simple class for storing environment variables
    """
    APP_NAME = "AI_CHAT"
    APP_KEYSPACE = f"{APP_NAME.lower()}_keyspace"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = os.environ.get('PORT', 8000)

    # router
    MAIN_ROUTER = "/api"

    # cassandra
    CASSANDRA_USERNAME = os.environ.get('CASSANDRA_USERNAME', 'admin')
    CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD', 'admin')
    CASSANDRA_HOST = os.environ.get('CASSANDRA_HOST', '0.0.0.0')
    CASSANDRA_PORT = os.environ.get('CASSANDRA_PORT', 9042)

    # web
    WEB_HOST = os.environ.get('WEB_HOST', 'http://localhost:3000')
