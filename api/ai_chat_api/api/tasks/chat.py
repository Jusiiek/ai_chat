import traceback
import time

from ai_chat_api.celery_app import celery_app
from ai_chat_api.api.models.chat import Chat
from ai_chat_api.api.models.message import Message, AuthorRoles
from ai_chat_api.api.protocols import models
from ai_chat_api.cassandradb import DatabaseManager


@celery_app.task(bind=True, max_retries=3)
def create_chat(
    self,
    thread_id: models.ID,
    user_id: models.ID,
    user_message: str
):
    try:
        db = DatabaseManager.get_instance()
        db.connect()

        chat = Chat.create(
            thread_id=thread_id,
            user_id=user_id,
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

        return chat.ai_message

    except Exception as e:
        print(f"Create thread task failed: {str(e)}")
        print(traceback.format_exc())
        self.retry(exc=e, countdown=30)
