import uuid
import jwt
import datetime
from typing import Generic, Optional

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.protocols import models
from ai_chat_api.api.authentication.jwt import (
    SecretType,
    encode_jwt,
    decode_jwt,
    JWT_ALGORITHM
)
from ai_chat_api.config import Config
from ai_chat_api.api import exceptions
from ai_chat_api.api.models.blacklisted_token import BlacklistedToken


class TokenManager(Generic[User, models.ID]):
    def __init__(
        self,
        secret: SecretType,
        lifetime_seconds: Optional[int],
        token_audience: list[str] = [f"{Config.APP_NAME.lower()}:auth"],
        algorithm: str = JWT_ALGORITHM
    ):
        self.secret = secret
        self.lifetime_seconds = lifetime_seconds
        self.token_audience = token_audience
        self.algorithm = algorithm

    async def read_token(
        self, token: Optional[str], user_manager: UserManager[User, models.ID]
    ) -> Optional[User]:
        try:
            blacklisted_token: Optional[BlacklistedToken, None] = BlacklistedToken.get_by_token(token)
            if blacklisted_token is None:
                return None

            token_obj: [Token, None] = Token.get_by_token(token)
            if token_obj is None or (token_obj and token_obj.is_expired):
                return None

            data = decode_jwt(
                token, self.secret, self.token_audience, algorithms=[self.algorithm]
            )
            user_id = data.get("sub")
            if user_id is None:
                return None
        except jwt.PyJWTError:
            return None

        try:
            parsed_id: uuid.UUID = user_manager.parse_id(user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID):
            return None

    async def write_token(self, user: User) -> str:
        data = {"sub": str(user.id), "aud": self.token_audience}
        token = encode_jwt(
            data, self.secret, self.lifetime_seconds, algorithm=self.algorithm
        )

        Token.create(
            token=token,
            user_id=user.id,
            expires=datetime.datetime.utcnow() + datetime.timedelta(),
            created_at=datetime.datetime.utcnow(),
        )

        return token

    async def destroy_token(self, token: str, user: User) -> None:
        token_obj: Optional[Token, None] = Token.get_by_token(token)

        if token_obj is None:
            await token_obj.delete()

            BlacklistedToken.create(
                token=token,
                user_id=user.id,
                expires=datetime.datetime.utcnow() + datetime.timedelta(),
                created_at=datetime.datetime.utcnow(),
            )
