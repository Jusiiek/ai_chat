from typing import Dict, Any

from fastapi import APIRouter

from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.authentication.authentication_backend import AuthenticationBackend
from ai_chat_api.api.manager import UserManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.protocols import models


def get_auth_router(
    backend: AuthenticationBackend[User, models.ID],
    user_manager: UserManager[User, models.ID],
    authenticator: Authenticator[User, models.ID],
    requires_verification: bool = False,
) -> APIRouter:
    """
    Creates a router with auth routes for an authentication backend.
    """

    router = APIRouter()
    get_current_user_token = authenticator.current_user_token(
        is_active=True, is_verified=requires_verification
    )

    login_response: Dict[str, Any] = {
        **backend.bearer_transport.get_success_login_response()
    }

    logout_response: Dict[str, Any] = {
        **backend.bearer_transport.get_success_logout_response()
    }

    return router
