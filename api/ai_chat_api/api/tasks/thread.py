from ai_chat_api.celery import celery_app

from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.protocols import models


def generate_title(message: str, max_length: int = 50) -> str:
    """
    Generates a thread title from the user message, ensuring it doesn’t cut words.
    """

    if len(message) <= max_length:
        return message
    return message[:max_length].rsplit(' ', 1)[0] + "…"


@celery_app.task
def create_thread(
    user_id: models.ID,
    user_message: str
):
    title = generate_title(user_message)

    thread = Thread.create(
        title=title,
        user_id=user_id,
    )

    Chat.create(
        thread_id=thread.id,
        user_id=user_id,
        user_message=user_message,
        ai_message="Hi, how can I help you?",
    )

    return thread.id
