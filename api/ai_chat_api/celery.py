from celery import Celery

from ai_chat_api.config import Config

celery_app = Celery(
    "ai_chat_worker",
    broker=Config.BROKER,
    backend=Config.BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# If using Cassandra as backend
celery_app.conf.update(
    cassandra_servers=["127.0.0.1:9042"],
    cassandra_keyspace="celeryks",
    cassandra_table="tasks_result"
)