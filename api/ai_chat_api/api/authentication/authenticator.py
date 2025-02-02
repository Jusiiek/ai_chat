import asyncio
from typing import Optional, Union

from fastapi import status, HTTPException

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.models.user import User


class Authenticator:
    """

    Gets the authenticated user

    It is responsible for authentication.
    If backend does not return a user, an HTTPException is thrown.

    Args
    -----------
    backend: AuthenticationBackend - a AuthenticationBackend instance
    user_manager: UserManager - a UserManager instance.
    """

    backend: AuthenticationBackend
    user_manager: UserManager

    def __init__(
        self,
        backend: AuthenticationBackend,
        user_manager: UserManager
    ):
        self.backend = backend
        self.user_manager = user_manager


    async def _authenticate(
        self,
        *args,
        optional: bool = False,
        is_active: bool = False,
        is_verified: bool = False,
        is_superuser: bool = False,
        **kwargs,
    ) -> tuple[Optional[dict], Optional[str]]:
        user: Union[User, None] = None
        token: Union[str, None] = kwargs.get("token", None)
        if token is not None:
            user = await self.backend.token_manager.read_token(token, self.user_manager)

        status_code = status.HTTP_401_UNAUTHORIZED
        if user:
            status_code = status.HTTP_403_FORBIDDEN
            if is_active and not user.is_active:
                status_code = status.HTTP_401_UNAUTHORIZED
                user = None
            elif is_verified and not user.is_verified or is_superuser and not user.is_superuser:
                user = None
        if not user and not optional:
            raise HTTPException(status_code=status_code)
        return user, token

    def get_current_user(
        self,
        optional: bool = False,
        is_active: bool = False,
        is_verified: bool = False,
        is_superuser: bool = False,
    ):
        async def current_user_dependency(*args, **kwargs):
            return await self._authenticate(
                *args,
                optional=optional,
                is_active=is_active,
                is_verified=is_verified,
                is_superuser=is_superuser,
                **kwargs
            )
        return current_user_dependency
