import re
from typing import Optional, Any, Dict, Tuple, Union, Generic

from ai_chat_api.api.authentication.jwt import SecretType
from ai_chat_api.api.authentication.password import PasswordHelper
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions
from ai_chat_api.api.schemas import user as user_schemas
from ai_chat_api.api.schemas import auth as auth_schemas


RESET_PASSWORD_TOKEN_AUDIENCE = "reset-password-token"
VERIFY_USER_TOKEN_AUDIENCE = "verify-user-token"


class UserManager(Generic[User, models.ID]):
    reset_password_token_secret: SecretType
    reset_password_token_lifetime_seconds: int = 3600
    reset_password_token_audience: str = RESET_PASSWORD_TOKEN_AUDIENCE

    verification_token_secret: SecretType
    verification_token_lifetime_seconds: int = 3600
    verification_token_audience: str = VERIFY_USER_TOKEN_AUDIENCE

    def __init__(
        self,
        user: User = None,
        password_helper: Optional[PasswordHelper] = None
    ):
        self.user = user
        if password_helper is None:
            self.password_helper = PasswordHelper()
        else:
            self.password_helper = password_helper

    async def _validate_password(self, password: str) -> bool:
        """
        Validates a password
        Parameters
        ----------
        password: str - The password to validate

        Returns
        -------
        result: bool - Whether the password is valid
        """
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        is_long_enough = len(password) >= 8

        if has_upper and has_lower and has_digit and has_special and is_long_enough:
            return True
        return False

    async def get(self, user_id: models.ID) -> User:
        """
        Gets a user with the given email
        Parameters
        ----------
        id: ID - The user's id

        Returns
        -------
        result: A user
        """

        user: Union[User, None] = await User.get_by_id(user_id)
        if user is None:
            raise exceptions.UserNotExists()

        self.user = user
        return user

    async def get_by_email(self, email: str) -> User:
        """
        Gets a user with the given email
        Parameters
        ----------
        email: str - The user's email

        Returns
        -------
        result: A user
        """

        user: Union[User, None] = await User.get_by_email(email)
        if user is None:
            raise exceptions.UserNotExists()

        self.user = user
        return user

    async def get_by_token(self, token: str) -> User:
        """
        Gets a user with the given email
        Parameters
        ----------
        token: str - A token that can be associated with a user.

        Returns
        -------
        result: A user
        """
        token_db: Union[Token, None] = await Token.get_by_token(token)
        if token_db is None:
            raise exceptions.InvalidVerifyToken()

        return await self.get(token.user_id)

    async def create(
        self,
        user_create: user_schemas.BCU
    ) -> User:
        """
        Creates a new user

        Parameters
        ----------
        user_create: UserCreate - The user to create schema to create

        Returns
        -------
        result: A new user.
        """
        ps_valid = await self._validate_password(user_create.password)
        if not ps_valid:
            raise exceptions.PasswordInvalid()

        is_user_exists = self.user.get_by_email(user_create.email)
        if not is_user_exists:
            raise exceptions.UserAlreadyExist()

        user_dict = user_create.create_update_dict()
        password = user_dict.pop('password')
        user_dict["hashed_password"] = self.password_helper.hash_password(password)

        created_user = await User.create(**user_dict)
        return created_user

    async def _update(
        self,
        user: User,
        update_dict: Dict[str, Any]
    ) -> User:
        """
        Validates sent data and updates a user
        Parameters
        ----------
        user: User - The user to update
        update_dict: dict - The updated data

        Returns
        -------
        updated_user: User - The updated user
        """
        validated_dict = {}
        for key, value in update_dict.items():
            if key == "email" and value != user.email:
                try:
                    await user.get_by_email(value)
                    raise exceptions.UserAlreadyExist()
                except exceptions.UserNotExists:
                    validated_dict[key] = value
            elif key == "password" and value is not None:
                await self._validate_password(value)
                validated_dict[key] = self.password_helper.hash_password(value)
            else:
                validated_dict[key] = value

        return await user.update(**validated_dict)

    async def update(
        self,
        user_update: user_schemas.BUU,
        user: User
    ):
        """
        Updates a user
        Parameters
        ----------
        user_update: UserUpdate - The updated data
        user: User - The user to update

        Returns
        -------
        updated_user: User - The updated user
        """
        updated_user_data = user_update.create_update_dict()
        updated_user = await self._update(user, updated_user_data)
        return updated_user

    async def delete(self, user: User) -> None:
        """
        Deletes a user

        Parameters
        ----------
        user: User - The user to delete

        Returns
        -------
        None
        """
        return await user.delete()

    async def validate_password(
        self,
        password: str,
        user: User
    ) -> Tuple[bool, Union[str, None]]:
        """
        Validates a user password

        Parameters
        ----------
        password: str - The password to validate
        user: User - The user to validate

        Returns
        -------
        valid: bool - Whether the password is valid
        """
        return await user.verify_password(password)

    async def authenticate(
        self,
        credentials: auth_schemas.APRF
    ) -> Optional[User]:
        try:
            user: User = await self.get_by_email(credentials.email)
        except exceptions.UserNotExists:
            return None

        verified, password_hash = self.password_helper.verify_password(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        if password_hash is None:
            await self._update(user, {"hashed_password": password_hash})

        return user
