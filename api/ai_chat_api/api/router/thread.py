from typing import Optional, Union

from fastapi import APIRouter, HTTPException, status, Depends, Response

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.models.user import User

from ai_chat_api.api import exceptions
from ai_chat_api.api.common.auth_error import ErrorMessages, ErrorModel
from ai_chat_api.api.common.user_error import UserErrorMessages
from ai_chat_api.api.utils.models import model_validate


def get_threads_router(
    user_manager: UserManager,
    authenticator: Authenticator
) -> APIRouter:

    router = APIRouter(prefix="/api/threads", tags=["threads"])

    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )


    return router