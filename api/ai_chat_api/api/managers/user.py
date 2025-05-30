import re
from typing import Optional, Any, Dict, Union

from fastapi import HTTPException, status

from ai_chat_api.api.authentication.password import PasswordHelper
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.protocols import models
from ai_chat_api.api import exceptions
from ai_chat_api.api.schemas.user import BaseCreateUser, BaseUpdateUser
from ai_chat_api.api.schemas.auth import AuthPasswordRequestForm
from ai_chat_api.api.managers import BaseManager
from ai_chat_api.api.common.password_error import (
    PasswordErrorMessages,
    PasswordErrorsHolder
)


RESET_PASSWORD_TOKEN_AUDIENCE = "reset-password-token"
VERIFY_USER_TOKEN_AUDIENCE = "verify-user-token"


class UserManager(BaseManager):
    def __init__(
        self,
        user: Union[User, None] = None,
        password_helper: Optional[PasswordHelper] = None
    ):
        super().__init__()
        self.user = user
        if password_helper is None:
            self.password_helper = PasswordHelper()
        else:
            self.password_helper = password_helper

    async def get_model_or_404(self, id: str) -> Optional[User]:
        try:
            parsed_id = self.parse_id(id)
            return await self.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

    async def _validate_password(self, password: str) -> PasswordErrorsHolder:
        """
        Validates a password
        Args
        ----------
        password: str - The password to validate

        Returns
        -------
        result: bool - Whether the password is valid
        """
        errors = []
        if not re.search(r'[A-Z]', password):
            errors.append(PasswordErrorMessages.PASSWORD_MISSING_UPPERCASE.value)

        if not re.search(r'[a-z]', password):
            errors.append(PasswordErrorMessages.PASSWORD_MISSING_LOWERCASE.value)

        if not re.search(r'\d', password):
            errors.append(PasswordErrorMessages.PASSWORD_MISSING_DIGIT.value)

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(PasswordErrorMessages.PASSWORD_MISSING_SPECIAL_CHAR.value)

        if len(password) < 8:
            errors.append(PasswordErrorMessages.PASSWORD_TOO_SHORT.value)

        return PasswordErrorsHolder(
            password=password,
            errors=errors,
            is_valid=len(errors) == 0,
        )

    async def get(self, user_id: models.ID) -> Union[User, None]:
        """
        Gets a user with the given email
        Args
        ----------
        user_id: ID - The user's id

        Returns
        -------
        result: A user
        """

        user: Union[User, None] = await User.get_by_id(user_id)
        if user is None:
            raise exceptions.UserNotExists()

        self.user = user
        return user

    async def get_by_email(self, email: str) -> Union[User, None]:
        """
        Gets a user with the given email
        Args
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

    async def get_by_token(self, token: str) -> Union[User, None]:
        """
        Gets a user with the given email
        Args
        ----------
        token: str - A token that can be associated with a user.

        Returns
        -------
        result: A user
        """
        token_db: Union[Token, None] = await Token.get_by_token(token)
        if token_db is None:
            raise exceptions.UserNotExists()

        return await self.get(token_db.user_id)

    async def create(
        self,
        user_create: BaseCreateUser
    ) -> User:
        """
        Creates a new user

        Args
        ----------
        user_create: UserCreate - The user to create schema to create

        Returns
        -------
        result: A new user.
        """
        password_errors_holder: PasswordErrorsHolder = (
            await self._validate_password(user_create.password)
        )
        if not password_errors_holder.is_valid:
            raise exceptions.PasswordInvalid(", ".join(password_errors_holder.errors))

        try:
            await self.get_by_email(user_create.email)
            raise exceptions.UserAlreadyExists()
        except exceptions.UserNotExists:
            pass

        user_dict = user_create.create_update_dict()
        password = user_dict.pop('password')
        user_dict["hashed_password"] = self.password_helper.hash_password(password)

        created_user = User.create(**user_dict)
        return created_user

    async def _update(
        self,
        user: User,
        update_dict: Dict[str, Any]
    ) -> User:
        """
        Validates sent data and updates a user
        Args
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
                    user_with_email = await user.get_by_email(value)
                    if user_with_email:
                        raise exceptions.UserAlreadyExists()
                except exceptions.UserNotExists:
                    validated_dict[key] = value
            elif key == "password":
                if value:
                    password_errors_holder: PasswordErrorsHolder = (
                        await self._validate_password(value)
                    )
                    if not password_errors_holder.is_valid:
                        raise exceptions.PasswordInvalid(
                            ", ".join(password_errors_holder.errors)
                        )
                    validated_dict["hashed_password"] = (
                        self.password_helper.hash_password(value))
            else:
                validated_dict[key] = value

        return user.update(**validated_dict)

    async def update(
        self,
        user_update: BaseUpdateUser,
        user: User
    ):
        """
        Updates a user
        Args
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

        Args
        ----------
        user: User - The user to delete

        Returns
        -------
        None
        """
        return user.delete()

    async def authenticate(
        self,
        credentials: AuthPasswordRequestForm
    ) -> Union[User, None]:
        try:
            user: User = await self.get_by_email(credentials.email)
        except exceptions.UserNotExists:
            return None

        verified = self.password_helper.verify_password(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        return user
