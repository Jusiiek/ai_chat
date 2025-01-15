from typing import Generic

from fastapi import Response, status

from ai_chat_api.api.protocols import models
from ai_chat_api.api.protocols.strategy import Strategy
from ai_chat_api.api.transports.bearer import BearerTransport
from ai_chat_api.api.exceptions import LogoutError
from ai_chat_api.api.models.user import User


class AuthenticationBackend(Generic[User, models.ID]):
	"""

	Authentication backend, they provide a full authentication method logic, login and logout

	Params
	------------------------
	bearer_transport: BearerTransport - Authentication transport instance.
	strategy: Strategy - Strategy instance.

	"""
	bearer_transport: BearerTransport
	strategy: Strategy

	def __init__(
		self,
		bearer_transport: BearerTransport,
		strategy: Strategy
	):
		self.bearer_transport = bearer_transport
		self.strategy = strategy

	async def login(
		self, strategy: Strategy[User, models.ID], user: User
	):
		token = await strategy.write_token(user)
		return await self.bearer_transport.get_login_response(token)

	async def logout(
		self, strategy: Strategy[User, models.ID], user: User, token: str
	) -> Response:
		try:
			await strategy.destroy_token(token, user)
		except LogoutError:
			pass

		try:
			response = await self.bearer_transport.get_logout_response()
		except LogoutError:
			response = Response(status_code=status.HTTP_204_NO_CONTENT)

		return response
