from typing import Union, Type

from fastapi import APIRouter, Depends, HTTPException, status

from ai_chat_api.api.backend.authentication import AuthenticationBackend
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.common.auth_error import ErrorMessages
from ai_chat_api.api.schemas.user import BaseUser, BaseCreateUser
from ai_chat_api.api.schemas.auth import AuthPasswordRequestForm
from ai_chat_api.api import exceptions
from ai_chat_api.api.utils.models import model_validate


def get_auth_router(
    backend: AuthenticationBackend,
    authenticator: Authenticator,
    user_manager: UserManager,
) -> APIRouter:

    router = APIRouter(prefix="/auth/jwt", tags=["/auth"])
    get_current_user_and_token = authenticator.get_current_user_and_token()

    login_responses: dict = {
        **backend.responses.get_success_login_response(),
        **backend.responses.get_unsuccessful_login_response()
    }
    logout_responses: dict = {
        **backend.responses.get_success_logout_response(),
    }

    register_responses: dict = {
        **backend.responses.get_unsuccessful_register_response()
    }

    @router.post("/login", responses=login_responses)
    async def login(
        credentials: AuthPasswordRequestForm
    ):
        user: Union[User, None] = await user_manager.authenticate(credentials)

        detail = None
        if user is None or not user.is_verified:
            detail = ErrorMessages.LOGIN_USER_NOT_VERIFIED.value,

        if user and not user.is_active:
            detail = ErrorMessages.LOGIN_BAD_CREDENTIALS.value

        if detail is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            )

        response = await backend.login(user)
        return response

    @router.post("/logout", responses=logout_responses)
    async def logout(
        user_token: tuple[User, str] = Depends(get_current_user_and_token)
    ):
        user, token = user_token
        return await backend.logout(token, user)

    @router.post(
        "/register",
        response_model=BaseUser,
        status_code=status.HTTP_201_CREATED,
        responses=register_responses
    )
    async def register(user_create_payload: BaseCreateUser):
        try:
            created_user = await user_manager.create(user_create_payload)
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.REGISTER_USER_ALREADY_EXISTS.value,
            )
        except exceptions.PasswordInvalid as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorMessages.REGISTER_INVALID_PASSWORD,
                    "reason": e.message,
                },
            )

        return model_validate(
            BaseUser,
            created_user
        )

    return router
