from typing import Generic

from fastapi import Response, status

from ai_chat_api.api.protocols import models
from ai_chat_api.api.protocols.auth_logic import AuthLogic
from ai_chat_api.api.transports.bearer import BearerTransport
from ai_chat_api.api.exceptions import LogoutError
from ai_chat_api.api.models.user import User


class AuthenticationBackend(Generic[User, models.ID]):
	"""

	Authentication backend, they provide a full authentication method logic, login and logout

	Params
	------------------------
	bearer_transport: BearerTransport - Authentication transport instance.
	security: AuthLogic - Security instance.

	"""
	bearer_transport: BearerTransport
	security: AuthLogic

	def __init__(
		self,
		bearer_transport: BearerTransport,
		security: AuthLogic
	):
		self.bearer_transport = bearer_transport
		self.security = security

	async def login(
		self, security: AuthLogic[User, models.ID], user: User
	):
		token = await security.write_token(user)
		return await self.bearer_transport.get_login_response(token)

	async def logout(
		self, security: AuthLogic[User, models.ID], user: User, token: str
	) -> Response:
		try:
			await security.destroy_token(token, user)
		except LogoutError:
			pass

		try:
			response = await self.bearer_transport.get_logout_response()
		except LogoutError:
			response = Response(status_code=status.HTTP_204_NO_CONTENT)

		return response
