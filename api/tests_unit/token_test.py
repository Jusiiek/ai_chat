from uuid import uuid4
from typing import Type

import pytest

from tests_unit.base_test import BaseTest
from ai_chat_api.api.models.base import BaseModel
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token


class TestToken(BaseTest):
    model: Type[BaseModel] = Token
    user_id = uuid4()

    @pytest.mark.asyncio
    async def test_object_creation(self):
        user = User.create(
            id=self.user_id,
            email="test_user_email@ai_app.com",
            hashed_password="hashed_password",
            is_active=True,
            is_superuser=False,
            is_verified=False
        )
        user.save()

        token = self.model.create(
            id=self.object_id,
            token="token",
            user_id=self.user_id,
            expire_at=None
        )
        token.save()

    @pytest.mark.asyncio
    async def test_get_object_by_id(self):
        base = await self.model.get_by_id(self.object_id)
        assert base is not None

    @pytest.mark.asyncio
    async def test_get_by_token(self):
        token = await self.model.get_by_token("token")
        assert token is not None

    @pytest.mark.asyncio
    async def test_get_by_user_id(self):
        token = await self.model.get_by_user_id(self.user_id)
        assert token is not None

    @pytest.mark.asyncio
    async def test_object_deletion(self):
        token = await self.model.get_by_id(self.object_id)
        user = await User.get_by_id(self.user_id)
        token.delete()
        user.delete()
