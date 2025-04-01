from datetime import datetime

from ai_chat_api.api.schemas.user import CreateUpdateModel
from ai_chat_api.api.protocols import models


class BaseCreateChat(CreateUpdateModel):
    user_message: str


class BaseChat(BaseCreateChat):
    user_id: models.ID
    ai_message: str
    id: models.ID
    created_at: datetime
    updated_at: datetime
