from datetime import datetime
from typing import Union

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.protocols import models


class Token(BaseModel):
    __table_name__ = 'token'

    token = columns.Text(primary_key=True)
    user_id = columns.UUID(index=True)
    expire_at = columns.DateTime()
    created_at = columns.DateTime(default=datetime.now())

    @classmethod
    async def get_by_token(cls, token: str) -> Union["Token", None]:
        return cls.objects.filter(token=token).allow_filtering().first()

    @classmethod
    async def get_by_user_id(cls, user_id: models.ID) -> Union["Token", None]:
        return cls.objects.filter(user_id=user_id).allow_filtering().first()
