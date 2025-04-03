from datetime import datetime

from ai_chat_api.api.schemas.user import CreateUpdateModel
from ai_chat_api.api.protocols import models


class BaseMessage(CreateUpdateModel):
    id: models.ID
    chat_id: models.ID
    author_role: str
    created_at: datetime
    updated_at: datetime
    content: str
