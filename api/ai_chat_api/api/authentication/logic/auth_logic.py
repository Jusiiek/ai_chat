from typing import Generic, Optional, Protocol

from ai_chat_api.api.manager import UserManager
from ai_chat_api.api.protocols import models


class AuthLogic(Protocol, Generic[models.UP, models.ID]):
    async def read_token(
        self, token: Optional[str], user_manager: UserManager[models.UP, models.ID]
    ) -> Optional[models.UP]: ...

    async def write_token(self, user: models.UP) -> str: ...

    async def destroy_token(
        self, token: str, user: models.UP
    ) -> None: ...
