import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from ai_chat_api.api.protocols.models import ID
from ai_chat_api.config import Config


class BaseModel(Model):
    __abstract__ = True
    __table_name__ = 'base_model'
    __keyspace__ = Config.APP_KEYSPACE

    id = columns.UUID(primary_key=True, default=uuid.uuid4)

    @classmethod
    async def create(cls, **kwargs):
        return await cls.create(**kwargs)

    @classmethod
    async def get_by_id(cls, model_id: ID):
        return await cls.get(id=model_id)
