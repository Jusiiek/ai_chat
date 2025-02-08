import os
import json

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.schemas.user import BaseCreateUser


FIXTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fixtures')


async def inject_users():
    user_manager: UserManager = UserManager()
    user_fixtures = os.path.join(FIXTURES_DIR, 'users.json')

    with open(user_fixtures, "r", encoding="utf-8") as file:
        users = json.load(file)

        for user in users:
            user_create = BaseCreateUser(**user)
            await user_manager.create(user_create)


async def inject_fixtures():
    await inject_users()
