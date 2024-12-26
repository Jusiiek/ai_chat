import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from ai_chat_api.api.protocols.models import ID


class BaseModel(Model):
    __keyspace__ = 'base_model'
    _table_name = 'base_model'
    id = columns.UUID(primary_key=True, default=uuid.uuid4)

    @classmethod
    async def create(cls, **kwargs):
        return await cls.create(**kwargs)

    @classmethod
    async def get_by_id(cls, model_id: ID):
        return await cls.get(id=model_id)
