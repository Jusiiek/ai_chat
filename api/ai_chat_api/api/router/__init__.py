from typing import Generic
from fastapi import APIRouter

from ai_chat_api.api.authentication.authentication_backend import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.protocols import models
from ai_chat_api.api.router.auth import get_auth_router


class Router(Generic[User, models.ID]):

    authenticator: Authenticator[User, models.ID]

    def __init__(
        self,
        user_manager: UserManager[User, models.ID],
        auth_back: AuthenticationBackend[User, models.ID]
    ):
        self.authenticator = Authenticator(auth_back, user_manager)
        self.user_manager = user_manager

    def get_auth_router(
        self,
        backend: AuthenticationBackend[User, models.ID],
        requires_verification: bool = False
    ) -> APIRouter:
        """

        Returns an authentication router for the given backend.

        Parameters
        ----------
        backend : AuthenticationBackend - The authentication backend instance.
        requires_verification (bool) - Whether the authentication backend requires the user to be verified.

        Returns
        ----------
        auth_router : APIRouter - The authentication router instance.

        """
        return get_auth_router(
            backend,
            self.authenticator,
            requires_verification
        )
