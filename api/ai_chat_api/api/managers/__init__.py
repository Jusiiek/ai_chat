import uuid
from typing import Any, Union, Optional

from fastapi import HTTPException, status

from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions


class BaseManager:
    model = BaseModel

    def __init__(self):
        pass

    def parse_id(self, model_id: Any) -> models.ID:
        """
        Parse a value into a correct ID type.

        Args
        ----------
        model_id: Any - Model ID as different type.

        Returns
        -------
        id: ID - Model correct ID
        """

        if isinstance(model_id, models.ID):
            return model_id
        try:
            return uuid.UUID(model_id)
        except ValueError as e:
            raise exceptions.InvalidID() from e

    async def get_model_or_404(self, id: str) -> Optional[BaseModel]:
        try:
            parsed_id = self.parse_id(id)
            return await self.get(parsed_id)
        except exceptions.DoesNotExist as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND) from e

    async def get(self, model_id: models.ID) -> Union[BaseModel, None]:
        pass
