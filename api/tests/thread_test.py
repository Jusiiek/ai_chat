import pytest

from fastapi import HTTPException
from ai_chat_api.api.managers.thread import ThreadManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.thread import Thread


def create_user():
    return User.create(
        email="test_user_to_update_and_delete@ai_app.com",
        hashed_password="T3stU3sr<>0",
        is_active=True,
        is_superuser=False,
        is_verified=True
    )


@pytest.mark.asyncio
async def test_get_model_404(thread_manager: ThreadManager):
    with pytest.raises(HTTPException):
        await thread_manager.get_model_or_404(
            "a914015a-73c6-4e55-8e92-f38d0b579122"
        )


@pytest.mark.asyncio
async def test_get_model_success(thread_manager: ThreadManager):
    user = create_user()
    thread = Thread.create(
        title="test_thread",
        user_id=user.id,
    )
    await thread_manager.get_model_or_404(thread.id)
    user.delete()
    thread.delete()


@pytest.mark.asyncio
async def test_create_model_success(thread_manager: ThreadManager):
    user = create_user()
    await thread_manager.create(
        user_id=user.id,
        user_message="test_message",
    )
    user.delete()
