from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from ai_chat_api.config import Config


class Task(Model):
    __keyspace__ = Config.APP_KEYSPACE
    __table_name__ = 'celery_task'

    task_id = columns.Text(primary_key=True)
    status = columns.Text(default='PENDING')
    result = columns.Bytes()
    date_done = columns.DateTime()
    traceback = columns.Blob()
    children = columns.Blob()
