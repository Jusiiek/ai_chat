from fastapi import Depends

from ai_chat_api.config import Config
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.managers.token import TokenManager
from ai_chat_api.api.responses.base import AuthResponse
from ai_chat_api.api.authentication.authentication_backend import AuthenticationBackend
from ai_chat_api.api.protocols import models


async def get_user_db():
    yield User


async def get_access_token_db():
    yield Token


async def get_user_manager(user_db: models.UserType = Depends(get_user_db)):
    yield UserManager(user_db)


def get_token_manager(access_token: Token = Depends(get_access_token_db)) -> TokenManager:
    return TokenManager(access_token, Config.TOKEN_LIFETIME)


auth_response: AuthResponse = AuthResponse("auth/jwt/login")
auth_backend: AuthenticationBackend = AuthenticationBackend(
    auth_response=auth_response,
    token_manager=get_token_manager,
)
