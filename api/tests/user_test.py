import pytest
from typing import Type

from tests.base_test import BaseTest
from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.models.user import User


class TestUser(BaseTest):
    model: Type[BaseModel] = User

    @pytest.mark.asyncio
    async def test_object_creation(self):
        user = self.model.create(
            id=self.object_id,
            email="test_user_email@ai_app.com",
            hashed_password="hashed_password",
            is_active=True,
            is_superuser=False,
            is_verified=False
        )
        user.save()

    @pytest.mark.asyncio
    async def test_get_object_by_id(self):
        base = await self.model.get_by_id(self.object_id)
        assert base is not None

    @pytest.mark.asyncio
    async def test_set_password(self):
        user = await self.model.get_by_id(self.object_id)
        await user.set_password("Gz7#pT2m!XvQ")

    @pytest.mark.asyncio
    async def test_verify_password(self):
        user = await self.model.get_by_id(self.object_id)
        assert await user.verify_password("Gz7#pT2m!XvQ")

    @pytest.mark.asyncio
    async def test_get_by_email(self):
        user: User = await self.model.get_by_email("test_user_email@ai_app.com")
        assert user is not None

    @pytest.mark.asyncio
    async def test_object_deletion(self):
        base = await self.model.get_by_id(self.object_id)
        base.delete()
        assert await self.model.get_by_id(self.object_id) is None
