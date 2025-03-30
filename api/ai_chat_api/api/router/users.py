from typing import Optional, Union

from fastapi import APIRouter, HTTPException, status, Depends, Response

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.models.user import User
from ai_chat_api.api.schemas.user import (
    BaseUser,
    BaseUpdateUser,
    BaseUpdateActiveUser
)
from ai_chat_api.api import exceptions
from ai_chat_api.api.common.auth_error import ErrorMessages, ErrorModel
from ai_chat_api.api.common.user_error import UserErrorMessages
from ai_chat_api.api.utils.models import model_validate


def get_users_router(
    user_manager: UserManager,
    authenticator: Authenticator
) -> APIRouter:

    user_model = BaseUser
    user_update_model = BaseUpdateUser

    router = APIRouter(prefix="/users", tags=["users"])

    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )
    get_current_superuser = authenticator.get_current_user(
        is_active=True, is_verified=True, is_superuser=True
    )

    get_or_update_user_responses = {
        status.HTTP_404_NOT_FOUND: {
            "description": UserErrorMessages.USER_DOES_NOT_EXIST.value,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": ErrorMessages.MISSING_TOKEN_OR_USER_IS_NOT_ACTIVE.value,
        },
    }

    bad_request_responses = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorMessages.USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": (
                                    ErrorMessages.USER_ALREADY_EXISTS.value
                                )
                            },
                        },
                        ErrorMessages.USER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": (
                                    ErrorMessages.USER_INVALID_PASSWORD.value,
                                )
                            },
                        },
                        ErrorMessages.USER_INVALID_CURRENT_PASSWORD: {
                            "summary": "Current password validation failed.",
                            "value": {
                                "detail": (
                                    ErrorMessages.USER_INVALID_CURRENT_PASSWORD.value,
                                )
                            },
                        },
                    }
                }
            },
        },
    }

    @router.get(
        "/active-user",
        response_model=user_model,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
    )
    async def me(user: User = Depends(get_current_active_user)):
        return model_validate(user_model, user)

    @router.put(
        "/active-user",
        response_model=user_model,
        dependencies=[Depends(get_current_active_user)],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
            **bad_request_responses
        },
    )
    async def update_me(
        user_update: BaseUpdateActiveUser,
        user: User = Depends(get_current_active_user),
    ):
        user_update_dict = user_update.dict()
        current_password: Union[str, None] = user_update_dict.get("current_password", None)
        new_password: Union[str, None] = user_update_dict.get("password", None)

        if new_password and current_password:
            is_current_password_valid = user.verify_password(
                current_password
            )

            if not is_current_password_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorMessages.USER_INVALID_CURRENT_PASSWORD,
                        "reason": "Current password is not correct.",
                    },
                )

        user_update = BaseUpdateUser(
            **user_update_dict.pop("current_password")
        )
        try:
            user_manager_instance = UserManager()
            user = await user_manager_instance.update(user_update, user)
            return model_validate(user_model, user)
        except exceptions.PasswordInvalid as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorMessages.USER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.USER_ALREADY_EXISTS.value,
            )

    async def get_user_or_404(id: str) -> Optional[User]:
        try:
            parsed_id = user_manager.parse_id(id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

    @router.get(
        "/{id}",
        response_model=user_model,
        dependencies=[Depends(get_current_superuser)],
        description="Get a user by id",
        status_code=status.HTTP_200_OK,
        responses={**get_or_update_user_responses}
    )
    async def get_user(user=Depends(get_user_or_404)):
        return model_validate(user_model, user)

    @router.put(
        "/{id}",
        response_model=user_model,
        dependencies=[Depends(get_current_superuser)],
        responses={
            **get_or_update_user_responses,
            **bad_request_responses,
            status.HTTP_403_FORBIDDEN: {
                "description": UserErrorMessages.NOT_A_SUPERUSER.value,
            },
        },
    )
    async def update_user(
        user_update: user_update_model,
        user=Depends(get_user_or_404),
    ):
        try:
            user_manager_instance = UserManager()
            user = await user_manager_instance.update(user_update, user)
            return model_validate(user_model, user)
        except exceptions.PasswordInvalid as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorMessages.USER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.USER_ALREADY_EXISTS.value,
            )

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        dependencies=[Depends(get_current_superuser)],
        responses={**get_or_update_user_responses}
    )
    async def delete_user(
        user=Depends(get_user_or_404),
    ):
        user_manager_instance = UserManager()
        await user_manager_instance.delete(user)
        return None

    return router
