from datetime import datetime
from typing import Union, List

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.protocols import models


class Chat(BaseModel):
    __tablename__ = 'chat'

    thread_id = columns.UUID(index=True)
    user_id = columns.UUID(index=True)
    created_at = columns.DateTime(default=datetime.now())
    updated_at = columns.DateTime(default=datetime.now())
    user_message: columns.Text = columns.Text(required=True)
    ai_message: columns.Text = columns.Text(required=True)

    @classmethod
    async def get_by_user_id(cls, user_id: models.ID) -> Union[List["Chat"], List]:
        return cls.objects.filter(user_id=user_id).allow_filtering()

    @classmethod
    async def get_by_thread_id(cls, thread_id: models.ID) -> Union[List["Chat"], List]:
        return cls.objects.filter(thread_id=thread_id).allow_filtering()
