from fastapi import APIRouter, status, Depends

from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.common.auth_error import ErrorMessages
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.managers.chat import ChatManager
from ai_chat_api.api.managers.thread import ThreadManager
from ai_chat_api.api.schemas.chat import (
    BaseCreateChat,
    BaseChat
)
from ai_chat_api.api.schemas.message import BaseMessage


def get_chats_router(
    authenticator: Authenticator,
    thread_manager: ThreadManager
) -> APIRouter:

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
        messages = []
        chat_messages = sorted(
            chat.get_messages,
            key=lambda msg: msg.created_at,
            reverse=False
        )
        for message in chat_messages:
            messages.append(
                BaseMessage(**message._as_dict())
            )
        return BaseChat(**chat._as_dict(), messages=messages)

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
        thread: Thread = Depends(thread_manager.get_model_or_404),
    ):
        return await chat_manager.create(
            thread.id,
            user.id,
            payload.user_message,
        )

    return router
