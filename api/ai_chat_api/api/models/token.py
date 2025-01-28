from typing import Optional

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.protocols import models


class Token(BaseModel):
    __table_name__ = 'token'

    token = columns.Text(primary_key=True)
    user_id = columns.UUID(index=True)
    expire_at = columns.DateTime()
    created_at = columns.DateTime()

    @classmethod
    async def get_by_token(cls, token: str) -> Optional["Token"]:
        return await cls.get(token)

    @classmethod
    async def get_by_user_id(cls, user_id: models.ID) -> Optional["Token"]:
        return await cls.get(user_id)
