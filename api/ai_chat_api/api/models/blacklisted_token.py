from datetime import datetime
from typing import Union

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel


class BlacklistedToken(BaseModel):
    __table_name__ = 'blacklisted_token'

    token = columns.Text(primary_key=True)
    user_id = columns.UUID(index=True)
    expired_at = columns.DateTime()
    created_at = columns.DateTime(default=datetime.now())

    @classmethod
    async def get_by_token(cls, token: str) -> Union["BlacklistedToken", None]:
        return cls.objects.filter(token=token).allow_filtering().first()
