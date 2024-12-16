from typing import Optional

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel


class BlacklistedToken(BaseModel):
    __keyspace__ = "blacklisted_token"

    token = columns.Text(primary_key=True)
    user_id = columns.UUID(index=True)
    expire_at = columns.DateTime()
    status = columns.Text(default="")

    @classmethod
    async def get_by_token(cls, token: str) -> Optional["BlacklistedToken"]:
        return await cls.get(token)
