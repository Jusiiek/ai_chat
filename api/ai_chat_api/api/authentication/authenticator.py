from typing import Generic, Optional

from ai_chat_api.api.manager import UserManager
from ai_chat_api.api.models.user import User
from ai_chat_api.api.protocols import models
from ai_chat_api.api.authentication.authentication_backend import AuthenticationBackend


class Authenticator(Generic[User, models.ID]):
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
		backend: AuthenticationBackend[User, models.ID],
		user_manager: UserManager[User, models.ID]
	):
		self.backend = backend
		self.user_manager = user_manager

	async def _authenticate(
		self,
		user_manager: UserManager[User, models.ID],
		is_active: bool = False,
		is_verified: bool = False,
		is_superuser: bool = False,
		**kwargs
	) -> tuple[Optional[User, None]]:
		"""
		Authenticates user

		Params
		-------------------
		user_manager: UserManager - user manager
		is_active: boolean - if is true, checks if user is active
		is_verified: boolean - if is true, checks if user is verified
		is_superuser: boolean - if is true, checks if user is superuser
		kwargs: keyword arguments
		"""
		user: Optional[User, None] = None
		token: Optional[str] = None

	def current_user_token(
		self,
		is_active: bool = False,
		is_verified: bool = False,
		is_superuser: bool = False,
	):
		pass
