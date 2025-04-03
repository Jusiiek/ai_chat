from datetime import datetime
from typing import List

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.models.message import Message
from ai_chat_api.api.protocols import models


class Chat(BaseModel):
    __table_name__ = 'chat'

    thread_id = columns.UUID(index=True)
    user_id = columns.UUID(index=True)
    created_at = columns.DateTime(default=datetime.now())
    updated_at = columns.DateTime(default=datetime.now())

    @classmethod
    async def get_by_user_id(cls, user_id: models.ID) -> List["Chat"]:
        return cls.objects.filter(user_id=user_id).allow_filtering()

    @classmethod
    async def get_by_thread_id(cls, thread_id: models.ID) -> List["Chat"]:
        return cls.objects.filter(thread_id=thread_id).allow_filtering()

    @property
    def get_messages(self) -> List[Message]:
        return Message.objects.filter(chat_id=self.id).allow_filtering()
