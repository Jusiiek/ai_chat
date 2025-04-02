from typing import Union, Optional

from fastapi import HTTPException, status

from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.managers import BaseManager
from ai_chat_api.api.tasks.thread import create_thread


class ThreadManager(BaseManager):
    async def get(self, thread_id: models.ID) -> Union[Thread, None]:
        """
        Gets a thread with the given id
        Args
        ----------
        thread_id: ID - The thread's id

        Returns
        -------
        result: A thread
        """

        thread: Union[Thread, None] = await Thread.get_by_id(thread_id)
        if thread is None:
            raise exceptions.DoesNotExist()

        return thread

    async def get_model_or_404(self, id: str) -> Optional[Thread]:
        try:
            parsed_id = self.parse_id(id)
            return await self.get(parsed_id)
        except exceptions.DoesNotExist as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from e

    async def create(self, user_id: models.ID, user_message: str) -> str:
        task = create_thread.delay(
            user_id,
            user_message,
        )
        return task.id
