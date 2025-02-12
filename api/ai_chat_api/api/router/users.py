from fastapi import APIRouter

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.authentication.authenticator import Authenticator


def get_users_router(
    user_manager: UserManager,
    authenticator: Authenticator
) -> APIRouter:

    router = APIRouter(prefix="/auth/jwt", tags=["/auth"])
    get_current_user = authenticator.get_current_user()

    return router