import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class BaseModel(Model):
    __keyspace__ = 'base_model'
    id = columns.UUID(primary_key=True, default=uuid.uuid4)

    @staticmethod
    def create(**kwargs): ...

    @staticmethod
    def get_by_id(model_id: uuid.UUID): ...

    @classmethod
    def update(cls, **kwargs): ...

    @classmethod
    def delete(cls): ...
