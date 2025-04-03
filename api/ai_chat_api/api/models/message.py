from enum import Enum
from datetime import datetime

from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel


class AuthorRoles(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    __table_name__ = "messages"

    chat_id = columns.UUID(index=True)
    author_role = columns.Text(required=False)
    created_at = columns.DateTime(default=datetime.now())
    updated_at = columns.DateTime(default=datetime.now())
    content = columns.Text()

    __primary_key__ = ('id', 'created_at')
