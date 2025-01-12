from typing import Generic, Optional, Protocol

from ai_chat_api.api.manager import UserManager
from ai_chat_api.api.protocols import models
from ai_chat_api.api.models.user import User


class AuthLogic(Protocol, Generic[User, models.ID]):
    async def read_token(
        self, token: Optional[str], user_manager: UserManager[User, models.ID]
    ) -> Optional[User]: ...

    async def write_token(self, user: User) -> str: ...

    async def destroy_token(
        self, token: str, user: User
    ) -> None: ...
