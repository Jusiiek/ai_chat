from http.client import HTTPException
from typing import Dict, Any, Optional

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.authentication.authentication_backend import AuthenticationBackend
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.managers.token import TokenManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.protocols import models


def get_auth_router(
    backend: AuthenticationBackend[User, models.ID],
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
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "detail": "You are not authorized to perform this action."
            }
        },
        **backend.bearer_transport.get_success_logout_response()
    }

    @router.post("/login", responses=login_response)
    async def login(
        credentials: OAuth2PasswordBearer = Depends(),
        user_manager: UserManager[User, models.ID] = Depends(get_current_user_token),
        token_manager: TokenManager[User, models.ID] = Depends(get_current_user_token),
    ):
        user: Optional[User, None] = await user_manager.authenticate(credentials)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LOGIN_BAD_CREDENTIALS"
            )

        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LOGIN_USER_NOT_VERIFIED",
            )

        return await backend.login(token_manager, user)

    @router.post("/logout", responses=logout_response)
    async def logout(
        user_and_token: tuple[User, str] = Depends(get_current_user_token),
        token_manager: TokenManager[User, models.ID] = Depends(get_current_user_token),
    ):
        user, token = user_and_token
        return await backend.logout(token_manager, user, token)

    return router
