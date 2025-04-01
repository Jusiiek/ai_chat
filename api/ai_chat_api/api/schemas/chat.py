from datetime import datetime

from ai_chat_api.api.schemas.user import CreateUpdateModel
from ai_chat_api.api.protocols import models


class BaseCreateChat(CreateUpdateModel):
    user_id: models.ID
    user_message: str
    ai_message: str


class BaseChat(BaseCreateChat):
    id: models.ID
    created_at: datetime
    updated_at: datetime
