import os


class Config:
    """
    A simple class for storing environment variables
    """
    APP_NAME = "AI_CHAT"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = os.environ.get('PORT', 8000)

    # cassandra
    CASSANDRA_USERNAME = os.environ.get('CASSANDRA_USERNAME', 'admin')
    CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD', 'admin')
    CASSANDRA_HOST = os.environ.get('CASSANDRA_HOST', '0.0.0.0')
    CASSANDRA_PORT = os.environ.get('CASSANDRA_PORT', 9042)
