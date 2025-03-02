import pytest
from uuid import uuid4
from typing import Type

from ai_chat_api.api.models.base import BaseModel


@pytest.mark.abstract
class BaseTest:
    model: Type[BaseModel] = BaseModel
    object_id = uuid4()

    @pytest.mark.asyncio
    async def test_object_creation(self):
        user = self.model.create(id=self.object_id)
        user.save()

    @pytest.mark.asyncio
    async def test_get_object_by_id(self):
        base = await self.model.get_by_id(self.object_id)
        assert base is not None

    @pytest.mark.asyncio
    async def test_object_deletion(self):
        base = await self.model.get_by_id(self.object_id)
        base.delete()
        assert await self.model.get_by_id(self.object_id) is None
