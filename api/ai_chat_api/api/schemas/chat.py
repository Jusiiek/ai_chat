from datetime import datetime
from typing import List

from ai_chat_api.api.schemas.user import CreateUpdateModel
from ai_chat_api.api.schemas.message import BaseMessage
from ai_chat_api.api.protocols import models


class BaseCreateChat(CreateUpdateModel):
    user_message: str


class BaseChat(CreateUpdateModel):
    user_id: models.ID
    id: models.ID
    created_at: datetime
    updated_at: datetime
    messages: List[BaseMessage]
