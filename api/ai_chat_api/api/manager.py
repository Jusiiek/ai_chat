from asyncio import exceptions
from typing import Optional

from ai_chat_api.api.authentication.jwt import (
    SecretType,
    decode_jwt,
    encode_jwt
)
from ai_chat_api.api.authentication.password import PasswordHelper
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions


RESET_PASSWORD_TOKEN_AUDIENCE = "reset-password-token"
VERIFY_USER_TOKEN_AUDIENCE = "verify-user-token"


class UserManager:
    reset_password_token_secret: SecretType
    reset_password_token_lifetime_seconds: int = 3600
    reset_password_token_audience: str = RESET_PASSWORD_TOKEN_AUDIENCE

    verification_token_secret: SecretType
    verification_token_lifetime_seconds: int = 3600
    verification_token_audience: str = VERIFY_USER_TOKEN_AUDIENCE

    def __init__(
        self,
         user: User,
         password_helper: Optional[PasswordHelper] = None
    ):
        self.user = user
        if password_helper is None:
            self.password_helper = PasswordHelper()
        else:
            self.password_helper = password_helper


    async def get(self, user_id: models.ID) -> models.UP:
        user = self.user.get_by_id(user_id)

        if user is None:
            raise exceptions.UserNotExist()

        return user

    async def get_by_email(self, email: str) -> models.UP:
        user = self.user.get_by_email(email)
        if user is None:
            raise exceptions.UserNotExist()

        return user

    async def get_by_token(self, token: str) -> models.UP:
        token_db: Token = Token.get_by_token(token)
        if token_db is None:
            raise exceptions.InvalidVerifyToken()

        return await self.get(token.user_id)