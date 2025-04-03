from typing import Union, Optional

from fastapi import HTTPException, status

from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.managers import BaseManager
from ai_chat_api.api.tasks.chat import create_chat


class ChatManager(BaseManager):
    async def get(self, chat_id: models.ID) -> Union[Chat, None]:
        """
        Gets a chat with the given id
        Args
        ----------
        chat_id: ID - The chat's id

        Returns
        -------
        result: A chat
        """

        chat: Union[Chat, None] = await Chat.get_by_id(chat_id)
        if chat is None:
            raise exceptions.DoesNotExist()

        return chat

    async def get_model_or_404(self, id: str) -> Optional[Chat]:
        try:
            parsed_id = self.parse_id(id)
            return await self.get(parsed_id)
        except exceptions.DoesNotExist as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from e

    async def create(
        self,
        thread_id: models.ID,
        user_id: models.ID,
        user_message: str,
    ) -> str:
        task = create_chat.delay(
            thread_id,
            user_id,
            user_message,
        )
        return task.id
