from fastapi import Depends

from ai_chat_api.config import Config

from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.responses.bearer import BearerResponse

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.managers.token import TokenManager

from ai_chat_api.api.router import Router


async def get_user_db():
    yield User


async def get_access_token_db():
    yield Token


bearer_response = BearerResponse()


async def get_user_manager(user: User = Depends(get_user_db)):
    yield UserManager(user)


def get_token_manager(
    token: Token = Depends(get_access_token_db),
) -> TokenManager:
    return TokenManager(token.token, lifetime_seconds=Config.TOKEN_LIFETIME)


backend = AuthenticationBackend(bearer_response, get_token_manager)
authenticator = Authenticator(backend=backend, user_manager=get_user_manager)


router = Router(user_manager=get_user_manager, backend=backend)
