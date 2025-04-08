import pytest

from fastapi import HTTPException
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.managers.chat import ChatManager
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


def create_thread(user_id):
    return Thread.create(
        user_id=user_id,
        title="test_thread",
    )


@pytest.mark.asyncio
async def test_get_model_404(chat_manager: ChatManager):
    with pytest.raises(HTTPException):
        await chat_manager.get_model_or_404(
            "a914015a-73c6-4e55-8e92-f38d0b579122"
        )


@pytest.mark.asyncio
async def test_get_model_success(chat_manager: ChatManager):
    user = create_user()
    thread = create_thread(user.id)
    chat = Chat.create(
        thread_id=thread.id,
        user_id=user.id,
    )

    await chat_manager.get_model_or_404(chat.id)

    user.delete()
    thread.delete()
    chat.delete()


@pytest.mark.asyncio
async def test_create_chat_success(chat_manager: ChatManager):
    user = create_user()
    thread = create_thread(user.id)
    await chat_manager.create(
        thread_id=thread.id,
        user_id=user.id,
        user_message="test_message",
    )
    user.delete()
    thread.delete()
