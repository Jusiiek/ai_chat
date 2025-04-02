from celery import Celery

from ai_chat_api.config import Config

celery_app = Celery(
    "ai_chat_worker",
    broker=Config.BROKER,
    backend=Config.BACKEND,
    include=["ai_chat_api.api.tasks.chat", "ai_chat_api.api.tasks.thread"]
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
)


celery_app.conf.update(
    cassandra_servers=["127.0.0.1:9042"],
    cassandra_keyspace="celeryks",
    cassandra_table="tasks_result"
)
celery_app.autodiscover_tasks(force=True)
