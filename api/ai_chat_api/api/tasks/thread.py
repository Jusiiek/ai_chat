import traceback
import time

from ai_chat_api.celery_app import celery_app
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.models.message import AuthorRoles, Message
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.protocols import models
from ai_chat_api.cassandradb import DatabaseManager


def generate_title(message: str, max_length: int = 50) -> str:
    """
    Generates a thread title from the user message, ensuring it doesn’t cut words.
    """

    if len(message) <= max_length:
        return message
    return message[:max_length].rsplit(' ', 1)[0] + "…"


@celery_app.task(bind=True, max_retries=3)
def create_thread(
    self,
    user_id: models.ID,
    user_message: str
):
    try:
        db = DatabaseManager.get_instance()
        db.connect()

        title = generate_title(user_message)

        thread = Thread.create(
            title=title,
            user_id=user_id,
        )

        chat = Chat.create(
            thread_id=thread.id,
            user_id=user_id
        )

        Message.create(
            chat_id=chat.id,
            content=user_message,
            author_role=AuthorRoles.USER.value
        )

        time.sleep(3)
        Message.create(
            chat_id=chat.id,
            content="Hi, how can I help you?",
            author_role=AuthorRoles.AI.value
        )

        return thread.id
    except Exception as e:
        print(f"Create thread task failed: {str(e)}")
        print(traceback.format_exc())
        self.retry(exc=e, countdown=30)
