from fastapi import APIRouter, status, Depends

from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.common.auth_error import ErrorMessages
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.managers.chat import ChatManager
from ai_chat_api.api.schemas.chat import (
    BaseCreateChat,
    BaseChat
)
from ai_chat_api.api.utils.models import model_validate


def get_chats_router(
    authenticator: Authenticator
)-> APIRouter:

    router = APIRouter(prefix="/api/chats", tags=["chats"])

    chat_manager = ChatManager()
    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )

    @router.get(
        "/{id}",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
        dependencies=[Depends(get_current_active_user)],
        response_model=BaseChat
    )
    async def get_chat(
        chat: Chat = Depends(chat_manager.get_model_or_404)
    ):
        return model_validate(BaseChat, chat)

    @router.post(
        "/{id}",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
    )
    async def create_chat(
        payload: BaseCreateChat,
        user: User = Depends(get_current_active_user),
    ):
        pass

    return router
