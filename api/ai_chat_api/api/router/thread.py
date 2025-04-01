from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends

from ai_chat_api.api.managers.thread import ThreadManager
from ai_chat_api.api.authentication.authenticator import Authenticator
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.schemas.thread import (
    BaseThread,
    BaseThreadList,
    BaseCreateThread
)

from ai_chat_api.api.common.auth_error import ErrorMessages
from ai_chat_api.api.utils.models import model_validate
from ai_chat_api.api import exceptions



def get_threads_router(
    authenticator: Authenticator
) -> APIRouter:

    router = APIRouter(prefix="/api/threads", tags=["threads"])
    thread_manager = ThreadManager()

    get_current_active_user = authenticator.get_current_user(
        is_active=True, is_verified=True
    )

    async def get_thread_or_404(id: str) -> Optional[Thread]:
        try:
            parsed_id = thread_manager.parse_id(id)
            return await thread_manager.get(parsed_id)
        except exceptions.DoesNotExist as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from e

    @router.get(
        "/",
        response_model=List[BaseThreadList],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
    )
    async def get_threads(
        user: User = Depends(get_current_active_user),

    ):
        if user.is_superuser:
            threads = Thread.objects.all()
        else:
            threads = Thread.get_by_user_id(user.id)

        serialized_data = [
            model_validate(
                BaseThreadList,
                {
                    "id": thread.id,
                    "title": thread.title,
                }
            ) for thread in threads
        ]

        return serialized_data


    @router.get(
        "/{id}",
        response_model=List[BaseThreadList],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": ErrorMessages.UNAUTHORIZED.value,
            },
        },
        dependencies=[Depends(get_current_active_user)],
    )
    async def get_thread(
        thread: Thread = Depends(get_thread_or_404),
    ):
        return model_validate(BaseThread, thread)

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
        pass


    return router
