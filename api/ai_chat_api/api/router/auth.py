from fastapi import APIRouter, Depends, HTTPException, Request, status

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.managers.user import UserManager


def get_auth_router(
    backend: AuthenticationBackend,
    authenticator: Authenticator,
    user_manager: UserManager,
) -> APIRouter:

    router = APIRouter()

    get_current_user = authenticator.get_current_user()

    return router