import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class BaseModel(Model):
    __keyspace__ = 'base_model'
    id = columns.UUID(primary_key=True, default=uuid.uuid4)

    @classmethod
    async def create(cls, **kwargs):
        return await cls.create(**kwargs)

    @classmethod
    async def get_by_id(cls, model_id: uuid.UUID):
        return await cls.get(id=model_id)

    @classmethod
    async def update(cls, **kwargs):
        return await cls.update(**kwargs)

    @classmethod
    async def delete(cls):
        return await cls.delete()
