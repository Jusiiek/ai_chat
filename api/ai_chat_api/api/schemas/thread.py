from datetime import datetime

from typing import Union, List

from ai_chat_api.api.schemas.user import CreateUpdateModel
from ai_chat_api.api.schemas.chat import BaseChat
from ai_chat_api.api.protocols import models


class BaseCreateThread(CreateUpdateModel):
    user_message: str


class BaseThread(CreateUpdateModel):
    id: models.ID
    user_id: models.ID
    title: str
    created_at: datetime
    updated_at: datetime
    conversations: Union[List[BaseChat], List]


class BaseThreadList(CreateUpdateModel):
    id: models.ID
    title: str
