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
    result_backend=(
        f'cassandra://{Config.CASSANDRA_HOST}:'
        f'{Config.CASSANDRA_PORT}/{Config.APP_KEYSPACE}'
    ),
    cassandra_servers=[Config.CASSANDRA_HOST],
    cassandra_keyspace=Config.APP_KEYSPACE,
    cassandra_table="celery_task"
)
celery_app.autodiscover_tasks(force=True)
