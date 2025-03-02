import pytest

from ai_chat_api.api import exceptions
from ai_chat_api.api.models.user import User
from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.managers.token import TokenManager
from ai_chat_api.api.schemas.user import BaseCreateUser


@pytest.mark.asyncio
async def test_create_user(user_manager: UserManager, user_schema_dict: dict):
    user_creation_schema = BaseCreateUser(**user_schema_dict)
    created_user = await user_manager.create(user_creation_schema)
    created_user.save()


def test_get_secret(token_manager: TokenManager):
    secret = "SECRET"
    secret_value = token_manager._get_secret_value(secret)
    assert type(secret_value) is str


@pytest.mark.asyncio
async def test_create_and_destroy_token(
    user_manager: UserManager,
    token_manager: TokenManager,
    user_schema_dict: dict
):
    user: User = await user_manager.get_by_email(user_schema_dict["email"])
    token = await token_manager.write_token(user)
    assert token is not None


@pytest.mark.asyncio
async def test_get_user_by_token(
    user_manager: UserManager,
    token_manager: TokenManager,
    user_schema_dict: dict
):
    user: User = await user_manager.get_by_email(user_schema_dict["email"])
    token = await token_manager.write_token(user)
    assert token is not None

    user_by_token: User = await user_manager.get_by_token(token)
    assert user_by_token.email == user.email


@pytest.mark.asyncio
async def test_read_token(
    user_manager: UserManager,
    token_manager: TokenManager,
    user_schema_dict: dict
):
    user: User = await user_manager.get_by_email(user_schema_dict["email"])
    token = await token_manager.write_token(user)
    assert token is not None
    assert user is not None
    user_by_token: User = await token_manager.read_token(token, user_manager)
    assert user_by_token is not None
    assert user_by_token.email == user.email
    await token_manager.destroy_token(token, user)


@pytest.mark.asyncio
async def test_read_token_with_no_existing_user(
    user_manager: UserManager,
    token_manager: TokenManager,
    user_schema_dict: dict
):
    with pytest.raises(exceptions.UserNotExists):
        new_user_schema = user_schema_dict.copy()
        new_user_schema["email"] = "test_user_email_4@ai_app.com"
        user_creation_schema = BaseCreateUser(**new_user_schema)
        created_user: User = await user_manager.create(user_creation_schema)
        token = await token_manager.write_token(created_user)
        created_user.delete()
        await token_manager.read_token(token, user_manager)
