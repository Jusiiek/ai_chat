from datetime import datetime
from typing import Tuple, Union, Optional

from ai_chat_api.api.models.base import BaseModel

from ai_chat_api.api.authentication.password import PasswordHelper


class User(BaseModel):
    _table_name = 'user'
    __keyspace__ = "user"

    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    edited_at: datetime

    async def set_password(
      self,
      password: str
    ) -> None:
        ph = PasswordHelper("")
        self.hashed_password = ph.hash_password(password)
        await self.save()

    async def verify_password(
        self,
        password: str
    ) -> Tuple[bool, Union[str, None]]:
        ph = PasswordHelper("")
        return ph.verify_password(password, self.hashed_password)

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        return cls.objects.get(email=email)
