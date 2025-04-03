from datetime import datetime, timedelta
from collections import defaultdict
from typing import List

from fastapi import APIRouter, status, Depends

from ai_chat_api.api.managers.thread import ThreadManager
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.schemas.thread import (
    BaseThread,
    BaseCreateThread
)
from ai_chat_api.api.schemas.message import BaseMessage
from ai_chat_api.api.schemas.chat import BaseChat

from ai_chat_api.api.common.auth_error import ErrorMessages


def get_threads_router(
    authenticator: Authenticator,
    thread_manager: ThreadManager
) -> APIRouter:

    router = APIRouter(prefix="/api/threads", tags=["threads"])

    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )

    @router.get(
        "/",
        response_model=dict,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Unauthorized access.",
            },
        },
    )
    async def get_threads(user: User = Depends(get_current_active_user)):
        if user.is_superuser:
            threads = Thread.objects.all()
        else:
            threads = Thread.get_by_user_id(user.id)

        today = datetime.utcnow().date()
        seven_days_ago = today - timedelta(days=7)
        thirty_days_ago = today - timedelta(days=30)

        categorized_threads = defaultdict(list)

        for thread in threads:
            created_date = thread.created_at.date()

            if created_date == today:
                categorized_threads["Today"].append(thread)
            elif created_date >= seven_days_ago:
                categorized_threads["Previous 7 days"].append(thread)
            elif created_date >= thirty_days_ago:
                categorized_threads["Previous 30 days"].append(thread)
            else:
                month_label = created_date.strftime("Previous %B")
                categorized_threads[month_label].append(thread)

        serialized_data = {
            category: [
                {
                    "id": thread.id,
                    "title": thread.title,
                }
                for thread in thread_list
            ]
            for category, thread_list in categorized_threads.items()
        }

        return serialized_data

    @router.get(
        "/{id}",
        response_model=BaseThread,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
        dependencies=[Depends(get_current_active_user)],
    )
    async def get_thread(
        thread: Thread = Depends(thread_manager.get_model_or_404),
    ):
        conversations = []
        for chat in await thread.conversations:
            messages = chat.get_messages
            conversations.append(
                BaseChat(
                    **chat._as_dict(),
                    messages=[
                        BaseMessage(**msg._as_dict())
                        for msg in messages
                    ]
                )
            )

        return BaseThread(
            **thread._as_dict(),
            conversations=conversations
        )

    @router.post(
        "/",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
    )
    async def create_thread(
        payload: BaseCreateThread,
        user: User = Depends(get_current_active_user),
    ):
        return await thread_manager.create(
            user.id,
            payload.user_message,
        )

    return router
