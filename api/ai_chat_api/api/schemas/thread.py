from datetime import datetime

from typing import Union, List

from ai_chat_api.api.schemas.user import CreateUpdateModel
from ai_chat_api.api.schemas.chat import BaseChat
from ai_chat_api.api.protocols import models


class BaseCreateThread(CreateUpdateModel):
    user_id: models.ID
    title: str


class BaseThread(BaseCreateThread):
    id: models.ID
    created_at: datetime
    updated_at: datetime
    conversations: Union[List[BaseChat], List]
