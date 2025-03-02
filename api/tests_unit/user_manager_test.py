import pytest

from uuid import UUID
from ai_chat_api.api import exceptions
from ai_chat_api.api.models.user import User
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.schemas.user import BaseCreateUser, BaseUpdateUser



def test_parse_id(user_manager: UserManager):
    random_string_id = "16fd2706-8baf-433b-82eb-8c7fada847da"
    parsed_id = user_manager.parse_id(random_string_id)
    assert type(parsed_id) is UUID


def test_parse_invalid_id(user_manager: UserManager):
    with pytest.raises(AttributeError):
        user_manager.parse_id(123.42)


@pytest.mark.asyncio
async def test_update_user(user_manager: UserManager, user_schema_dict: dict):
    update_dict = {"password": "Gz7#pT2m!XvW"}
    user: User = await user_manager.get_by_email(user_schema_dict["email"])
    user_creation_schema = BaseUpdateUser(**update_dict)
    await user_manager.update(user_creation_schema, user)


@pytest.mark.asyncio
async def test_invalid_user_creation_with_password(user_manager: UserManager, user_schema_dict: dict):
    with pytest.raises(exceptions.PasswordInvalid):
        new_user_schema = user_schema_dict.copy()
        new_user_schema["password"] = "123"
        new_user_schema["email"] = "test_user_email_2@ai_app.com"
        user_creation_schema = BaseCreateUser(**new_user_schema)
        await user_manager.create(user_creation_schema)


@pytest.mark.asyncio
async def test_invalid_user_creation_with_email(user_manager: UserManager, user_schema_dict: dict):
    with pytest.raises(exceptions.UserAlreadyExists):
        new_user_schema = user_schema_dict.copy()
        new_user_schema["email"] = "test_user_email@ai_app.com"
        user_creation_schema = BaseCreateUser(**new_user_schema)
        await user_manager.create(user_creation_schema)


@pytest.mark.asyncio
async def test_invalid_user_update_password(user_manager: UserManager, user_schema_dict: dict):
    with pytest.raises(exceptions.PasswordInvalid):
        new_user_schema = user_schema_dict.copy()
        new_user_schema["password"] = "123"
        user_creation_schema = BaseCreateUser(**new_user_schema)
        await user_manager.create(user_creation_schema)


@pytest.mark.asyncio
async def test_delete_user(user_manager: UserManager, user_schema_dict: dict):
    user: User = await user_manager.get_by_email(user_schema_dict["email"])
    await user_manager.delete(user)
