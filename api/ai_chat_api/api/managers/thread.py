import uuid
from typing import Any, Union

from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions
from ai_chat_api.api.models.thread import Thread


class ThreadManager:
    def __init__(self):
        pass

    def parse_id(self, thread_id: Any) -> models.ID:
        """
        Parse a value into a correct ID type.

        Args
        ----------
        thread_id: Any - Thread ID as different type.

        Returns
        -------
        id: ID - Thread correct ID
        """

        if isinstance(thread_id, models.ID):
            return thread_id
        try:
            return uuid.UUID(thread_id)
        except ValueError as e:
            raise exceptions.InvalidID() from e

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
