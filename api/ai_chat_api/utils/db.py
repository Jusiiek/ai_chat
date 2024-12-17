from cassandra.cqlengine.management import (
	sync_table,
	drop_table
)

from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.models.blacklisted_token import BlacklistedToken


MODELS = [User, Token, BlacklistedToken]


async def drop_db():
	for model in MODELS:
		try:
			await drop_table(model)
			print(f"Successfully dropped table for model: {model.__name__}")
		except Exception as e:
			print(f"Failed to drop table for model {model.__name__}: {e}")


async def create_db():
	for model in MODELS:
		try:
			await sync_table(model)
			print(f"Successfully created table for model: {model.__name__}")
		except Exception as e:
			print(f"Failed to create table for model: {model.__name__}: {e}")
