from datetime import datetime
from typing import Union
from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel

from ai_chat_api.api.authentication.password import PasswordHelper


class User(BaseModel):
    __table_name__ = 'user'

    email = columns.Text(primary_key=True)
    hashed_password = columns.Text()
    is_active = columns.Boolean(default=False)
    is_superuser = columns.Boolean(default=False)
    is_verified = columns.Boolean(default=False)
    created_at = columns.DateTime(default=datetime.now())
    edited_at = columns.DateTime(default=datetime.now())

    async def set_password(
        self,
        password: str
    ) -> None:
        """
        Set user password

        Args
        -----------------
        password: str - New user password
        """
        ph = PasswordHelper("")
        self.hashed_password = ph.hash_password(password)
        self.save()

    async def verify_password(
        self,
        password: str
    ) -> bool:
        """
        Verify user password

        Args
        ---------------------
        password: str - User password

        Returns
        ---------------------
        is_valid: bool - User password is valid or not
        """
        ph = PasswordHelper("")
        return ph.verify_password(password, self.hashed_password)

    @classmethod
    async def get_by_email(cls, email: str) -> Union["User", None]:
        return cls.objects.filter(email=email).allow_filtering().first()
