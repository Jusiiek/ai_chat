from datetime import datetime
from typing import List

from cassandra.cqlengine import columns

from ai_chat_api.api.protocols import models
from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.models.chat import Chat


class Thread(BaseModel):
    __table_name__ = 'thread'

    user_id = columns.UUID(index=True)
    title = columns.Text()
    created_at = columns.DateTime(default=datetime.now())
    updated_at = columns.DateTime(default=datetime.now())

    @property
    async def conversations(self) -> List[Chat]:
        """
        Fetch conversations dynamically using thread_id.
        """
        return await Chat.get_by_thread_id(thread_id=self.id)

    @classmethod
    async def get_by_user_id(cls, user_id: models.ID) -> List["Thread"]:
        return cls.objects.filter(user_id=user_id).allow_filtering()
