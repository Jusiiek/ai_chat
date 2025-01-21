from typing import Generic, Optional, Any

from fastapi import HTTPException, status

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.protocols import models
from ai_chat_api.api.authentication.authentication_backend import AuthenticationBackend


class Authenticator(Generic[models.UserType, models.ID]):
	"""

	Performs the authentication.

	Params
	---------------------
	backend: AuthenticationBackend - authentication backend
	user_manager: UserManager - user manager

	"""
	backend: AuthenticationBackend

	def __init__(
		self,
		backend: AuthenticationBackend[models.UserType, models.ID],
		user_manager: UserManager[models.UserType, models.ID]
	):
		self.backend = backend
		self.user_manager = user_manager

	async def _authenticate(
		self,
		user_manager: UserManager[models.UserType, models.ID],
		is_active: bool = False,
		is_verified: bool = False,
		is_superuser: bool = False,
		**kwargs
	) -> tuple[Optional[models.UserType], Optional[str]]:
		"""
		Authenticates user

		Params
		-------------------
		user_manager: UserManager - user manager
		is_active: boolean - 'if is true, checks if user is active.
		If not throws exception with status unauthorized. Defaults to False.'
		is_verified: boolean - 'if is true, checks if user is verified.
		If not throws exception with status forbidden. Defaults to False.'
		is_superuser: boolean - 'if is true, checks if user is superuser.
		If not throws exception with status forbidden. Defaults to False.'
		kwargs: keyword arguments

		Returns
		-------------------
		user: User - user
		token: str - token
		"""
		user: Optional[models.UserType, None] = None
		token: Optional[str] = kwargs.pop("token", None)

		if token:
			user: Optional[models.UserType, None] = self.backend.token_manager.read_token(token, user_manager)

		status_code = status.HTTP_401_UNAUTHORIZED
		if user:
			status_code = status.HTTP_403_FORBIDDEN
			if is_active and not user.is_active:
				status_code = status.HTTP_401_UNAUTHORIZED
				user = None
			elif is_verified and not user.is_verified or is_superuser and not user.is_superuser:
				user = None

		if not user:
			raise HTTPException(status_code=status_code)
		return user, token

	def current_user_token(
		self,
		is_active: bool = False,
		is_verified: bool = False,
		is_superuser: bool = False,
	):

		async def current_user_token_dependency(*args: Any, **kwargs: Any):
			await self._authenticate(
				self.user_manager,
				is_active=is_active,
				is_verified=is_verified,
				is_superuser=is_superuser,
				**kwargs
			)

		return current_user_token_dependency
