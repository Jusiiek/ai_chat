from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Request, Response

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.models.user import User
from ai_chat_api.api.schemas.user import (
    BaseUser,
    BaseCreateUser,
    BaseUpdateUser
)
from ai_chat_api.api import exceptions
from ai_chat_api.api.common.auth_error import ErrorMessages, ErrorModel
from ai_chat_api.api.common.user_error import UserErrorMessages
from ai_chat_api.api.utils.models import model_validate


def get_users_router(
    user_manager: UserManager,
    authenticator: Authenticator
) -> APIRouter:

    router = APIRouter(prefix="/users", tags=["users"])

    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )
    get_current_superuser = authenticator.get_current_user(
        is_active=True, is_verified=True, is_superuser=True
    )

    get_user_manager = authenticator.get_user_manager(
        is_active=True, is_verified=True, is_superuser=True
    )

    get_or_update_user_responses = {
        status.HTTP_404_NOT_FOUND: {
            "description": UserErrorMessages.USER_DOES_NOT_EXIST.value,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": UserErrorMessages.NOT_A_SUPERUSER.value,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": ErrorMessages.MISSING_TOKEN_OR_USER_IS_NOT_ACTIVE.value,
        },
    }

    async def get_user_or_404(id: str) -> Optional[User]:
        try:
            parsed_id = user_manager.parse_id(id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


    @router.get(
        "/{id}",
        response_model=BaseUser,
        dependencies=[Depends(get_current_superuser)],
        description="Get a user by id",
        status_code=status.HTTP_200_OK,
        responses={**get_or_update_user_responses}
    )
    async def get_user(user=Depends(get_user_or_404)):
        return model_validate(BaseUser, user)

    @router.put(
        "/{id}",
        response_model=BaseUser,
        dependencies=[Depends(get_current_superuser)],
        responses={
            **get_or_update_user_responses,
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
                        }
                    }
                },
            },
        },
    )
    async def update_user(
        user_update: BaseUpdateUser,  # type: ignore
        user=Depends(get_user_or_404),
        user_manager_instance: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager_instance.update(user_update, user)
            return model_validate(BaseUser, user)
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
        name="users:delete_user",
        responses={**get_or_update_user_responses}
    )
    async def delete_user(
        user=Depends(get_user_or_404),
        user_manager_instance: UserManager = Depends(get_user_manager),
    ):
        await user_manager_instance.delete(user)
        return None


    return router