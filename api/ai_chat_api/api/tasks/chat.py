from ai_chat_api.celery import celery_app

from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.protocols import models


@celery_app.task
def create_chat(
    thread_id: models.ID,
    user_id: models.ID,
    user_message: str
):
    chat = Chat.create(
        thread_id=thread_id,
        user_id=user_id,
        user_message=user_message,
        ai_message="Hi, how can I help you?",
    )

    return chat.ai_message
