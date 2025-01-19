from typing import Generic

from fastapi import Response, status

from ai_chat_api.api.protocols import models
from ai_chat_api.api.responses.auth import AuthResponse
from ai_chat_api.api.exceptions import LogoutError
from ai_chat_api.api.models.user import User
from ai_chat_api.api.managers.token import TokenManager


class AuthenticationBackend(Generic[User, models.ID]):
	"""

	Authentication backend, they provide a full authentication method logic, login and logout

	Params
	------------------------
	auth_response: AuthResponse - Authentication response instance.
	token_manager: TokenManager - Token manager instance.

	"""
	token_manager: TokenManager
	auth_response: AuthResponse

	def __init__(
		self,
		token_manager: TokenManager,
		auth_response: AuthResponse
	):
		self.token_manager = token_manager
		self.auth_response = auth_response

	async def login(
		self, token_manager: TokenManager[User, models.ID], user: User
	):
		token = await token_manager.write_token(user)
		return await self.auth_response.get_login_response(token)

	async def logout(
		self, token_manager: TokenManager[User, models.ID], user: User, token: str
	) -> Response:
		try:
			await token_manager.destroy_token(token, user)
		except LogoutError:
			pass

		try:
			response = await self.auth_response.get_logout_response()
		except LogoutError:
			response = Response(status_code=status.HTTP_204_NO_CONTENT)

		return response
