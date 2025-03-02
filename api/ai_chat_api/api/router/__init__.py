from fastapi import APIRouter

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.router.auth import get_auth_router
from ai_chat_api.api.router.users import get_users_router


class Router:

    def __init__(
        self,
        user_manager: UserManager,
        backend: AuthenticationBackend
    ):
        self.authenticator = Authenticator(backend, user_manager)
        self.user_manager = user_manager

    def get_auth_router(self) -> APIRouter:
        """

        Returns an authentication router for the given backend.

        Returns
        ----------
        auth_router : APIRouter - The authentication router instance.

        """
        return get_auth_router(
            self.authenticator.backend,
            self.authenticator,
            self.user_manager
        )

    def get_users_router(self) -> APIRouter:
        return get_users_router(
            self.user_manager,
            self.authenticator,
        )
