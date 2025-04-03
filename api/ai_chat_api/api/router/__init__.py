from fastapi import APIRouter

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.managers.thread import ThreadManager
from ai_chat_api.api.router.auth import get_auth_router
from ai_chat_api.api.router.users import get_users_router
from ai_chat_api.api.router.thread import get_threads_router
from ai_chat_api.api.router.chat import get_chats_router
from ai_chat_api.api.router.tasks import get_tasks_router


class Router:

    def __init__(
        self,
        user_manager: UserManager,
        backend: AuthenticationBackend
    ):
        self.authenticator = Authenticator(backend, user_manager)
        self.user_manager = user_manager
        self.thread_manager = ThreadManager()

    def get_auth_router(self) -> APIRouter:
        """
        Returns an authentication router for the given backend.

        Returns
        ----------
        router : APIRouter - The authentication router instance.
        """
        return get_auth_router(
            self.authenticator.backend,
            self.authenticator,
            self.user_manager
        )

    def get_users_router(self) -> APIRouter:
        """
        Returns a users router.

        Returns
        ----------
        router : APIRouter - The user router instance.
        """
        return get_users_router(
            self.user_manager,
            self.authenticator,
        )

    def get_thread_router(self) -> APIRouter:
        """
        Returns a thread router.

        Returns
        ----------
        router : APIRouter - The thread router instance.
        """
        return get_threads_router(
            self.authenticator,
            self.thread_manager
        )

    def get_chats_router(self) -> APIRouter:
        """
        Returns a chat router.

        Returns
        ----------
        router : APIRouter - The chat router instance.
        """
        return get_chats_router(
            self.authenticator,
            self.thread_manager
        )

    def get_tasks_router(self) -> APIRouter:
        """
        Returns a tasks router.

        Returns
        ----------
        router : APIRouter - The tasks router instance.
        """
        return get_tasks_router(
            self.authenticator
        )
