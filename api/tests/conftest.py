from typing import Optional, Union

import pytest

from ai_chat_api.config import Config
from ai_chat_api.api.models.user import User
from ai_chat_api.cassandradb import DatabaseManager
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.responses.auth import AuthResponse
from ai_chat_api.api.responses.bearer import BearerResponse
from ai_chat_api.api.authentication.password import PasswordHelper
from ai_chat_api.api.managers.token import TokenManager, SecretType
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.backend.authentication import AuthenticationBackend


@pytest.fixture(scope="session", autouse=True)
def setup_cassandra():
    db = DatabaseManager.get_instance()
    db.connect()


class BearerResponseTest(BearerResponse):
    def __init__(self, tokenUrl):
        super().__init__(tokenUrl)


class TokenManagerTest(TokenManager):
    def __init__(
        self,
        secret: SecretType,
        lifetime_seconds: Optional[int],
        token_audience: list[str] = [f"{Config.APP_NAME.lower()}:auth"],
        algorithm: str = Config.JWT_ALGORITHM
    ):
        super().__init__(
            secret,
            lifetime_seconds,
            token_audience,
            algorithm
        )


class UserManagerTest(UserManager):
    def __init__(
        self,
        user: Union[User, None] = None,
        password_helper: Optional[PasswordHelper] = None
    ):
        super().__init__(user, password_helper)


class AuthenticationBackendTest(AuthenticationBackend):
    def __init__(
        self,
        responses: AuthResponse,
        token_manager: TokenManager
    ):
        super().__init__(responses, token_manager)


class AuthenticatorTest(Authenticator):
    def __init__(
        self,
        backend: AuthenticationBackend,
        user_manager: UserManager
    ):
        super().__init__(backend, user_manager)


@pytest.fixture
def user_schema_dict() -> dict:
    return {
        "email": "test_user_email@ai_app.com",
        "password": "Gz7#pT2m!XvQ",
    }


@pytest.fixture
def response() -> BearerResponse:
    return BearerResponse("/login")


@pytest.fixture
def token_manager() -> TokenManager:
    return TokenManager("SECRET", Config.TOKEN_LIFETIME)


@pytest.fixture
def user_manager() -> UserManager:
    return UserManager()


@pytest.fixture
def authentication_backend() -> AuthenticationBackend:
    return AuthenticationBackend(
        responses=BearerResponseTest("/login"),
        token_manager=TokenManagerTest("SECRET", Config.TOKEN_LIFETIME)
    )
