from ai_chat_api.config import Config

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.responses.bearer import BearerResponse

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.managers.token import TokenManager

from ai_chat_api.api.router import Router


SECRET = "SECRET"


bearer_response = BearerResponse(tokenUrl="auth/jwt/login")
user_manager = UserManager()
token_manager = TokenManager(SECRET, Config.RESET_PASSWORD_TOKEN_LIFETIME)

backend = AuthenticationBackend(responses=bearer_response, token_manager=token_manager)
authenticator = Authenticator(backend=backend, user_manager=user_manager)

router = Router(user_manager=user_manager, backend=backend)
