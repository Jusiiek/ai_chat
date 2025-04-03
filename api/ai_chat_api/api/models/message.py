from uuid import uuid1
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
    created_at_id = columns.TimeUUID(primary_key=True)
    created_at = columns.DateTime(required=True)
    updated_at = columns.DateTime(required=True)
    content = columns.Text()
