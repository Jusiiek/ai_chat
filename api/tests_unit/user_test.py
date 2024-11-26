from ai_chat_api.api.manager import UserManager
from cassandra.cqlengine.management import sync_table
from ai_chat_api.api.models.user import User


USER_DICT = {
	"email": "test_create_1@gmail.com",
	"password": "12zaqWSX!@",
}


user_manager = UserManager()


async def test_create_user():
	sync_table(User)
	created_user = await user_manager.create(USER_DICT)
	assert created_user.email == USER_DICT["email"]


async def test_update_user():
	user = await user_manager.get_by_email(USER_DICT["email"])
	updated_dict = USER_DICT.copy()
	updated_dict["email"] = "test_create_2@gmail.com"
	updated_user = await user_manager.update(updated_dict, user)
	assert updated_user.email == updated_dict["email"]


async def test_delete_user():
	user = await user_manager.get_by_email("test_create_2@gmail.com")
	await user_manager.delete(user)
