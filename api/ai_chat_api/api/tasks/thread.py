import traceback
from datetime import datetime
import time
import uuid

from ai_chat_api.celery_app import celery_app
from ai_chat_api.api.models.thread import Thread
from ai_chat_api.api.models.message import AuthorRoles, Message
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.protocols import models
from ai_chat_api.cassandradb import DatabaseManager
from ai_chat_api.ai_model.model import model_instance


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
            author_role=AuthorRoles.USER.value,
            created_at_id=uuid.uuid1(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        time.sleep(4)
        model_response = model_instance.generate_response(user_message)

        Message.create(
            chat_id=chat.id,
            content=model_response,
            author_role=AuthorRoles.AI.value,
            created_at_id=uuid.uuid1(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return thread.id
    except Exception as e:
        print(f"Create thread task failed: {str(e)}")
        print(traceback.format_exc())
        self.retry(exc=e, countdown=30)
