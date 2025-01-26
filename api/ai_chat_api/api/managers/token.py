import uuid
import jwt
from datetime import timedelta, datetime
from typing import Generic, Optional, List, Dict, Any, Union
from pydantic import SecretStr, SecretType

from ai_chat_api.api.managers.user import UserManager
from ai_chat_api.api.models.token import Token
from ai_chat_api.api.models.blacklisted_token import BlacklistedToken
from ai_chat_api.api.protocols import models
from ai_chat_api.config import Config
from ai_chat_api.api import exceptions


SecretType = Union[str, SecretStr]


class TokenManager(Generic[models.UserType, models.ID]):
    """
    Token manager is a class used to manage tokens such as creating, reading or deleting.

    Parameters
    -------------
    secret: Secret - Token model
    lifetime_seconds: Optional[int] - Token lifetime in seconds
    token_audience: list[str] = List of audience
    algorithm: str = JWT_ALGORITHM - algorithm used to sign the token.

    """

    def __init__(
        self,
        secret: SecretType,
        lifetime_seconds: Optional[int],
        token_audience: list[str] = [f"{Config.APP_NAME.lower()}:auth"],
        algorithm: str = Config.JWT_ALGORITHM
    ):
        self.secret = secret
        self.lifetime_seconds = lifetime_seconds
        self.token_audience = token_audience
        self.algorithm = algorithm

    def _get_secret_value(self, secret: SecretType) -> str:
        """
        Return value of a secret.

        Returns
        --------
        secret: str - secret value
        """
        if isinstance(secret, SecretStr):
            return secret.get_secret_value()
        return secret

    def _encode_jwt(
        self,
        data: dict,
        secret: SecretType,
        lifetime_seconds: Optional[int] = None,
        algorithm: str = Config.JWT_ALGORITHM,
    ) -> str:
        """
        Returns JWT encoded jwt.

        Parameters
        ----------
        data : dict - user data to encode
        secret : SecretType - jwt secret
        lifetime_seconds : optional in

        Returns
        -----------
        token: str - JWT encoded jwt
        """
        payload = data.copy()
        if lifetime_seconds:
            expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
            payload["exp"] = expire
        return jwt.encode(payload, self._get_secret_value(secret), algorithm=algorithm)

    def _decode_jwt(
        self,
        encoded_jwt: str,
        secret: SecretType,
        audience: List[str],
        algorithms: List[str] = [Config.JWT_ALGORITHM],
    ) -> Dict[str, Any]:
        """
        Decodes JWT encoded jwt.

        Parameters
        ------------------
        encoded_jwt : str - JWT encoded jwt
        secret : SecretType - jwt secret
        audience : List[str] - list of audience
        algorithms : List[str] - list of algorithm

        Returns
        ---------------
        Decoded JWT data
        """
        return jwt.decode(
            encoded_jwt,
            self._get_secret_value(secret),
            audience=audience,
            algorithms=algorithms
        )

    async def read_token(
        self, token: Optional[str], user_manager: UserManager[models.UserType, models.ID]
    ) -> Optional[models.UserType]:
        try:
            blacklisted_token: Optional[BlacklistedToken, None] = BlacklistedToken.get_by_token(token)
            if blacklisted_token is not None:
                return None

            token_obj: [Token, None] = Token.get_by_token(token)
            if token_obj is not None and token_obj.is_expired:
                return None

            data = self._decode_jwt(
                token, self.secret, self.token_audience, algorithms=[self.algorithm]
            )
            user_id = data.get("sub")
            if user_id is None:
                return None
        except jwt.PyJWTError:
            return None

        try:
            parsed_id: uuid.UUID = user_manager.parse_id(user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID):
            return None

    async def write_token(self, user: models.UserType) -> str:

        token: Optional[Token, None] = Token.get_by_user_id(user.id)
        if token is not None:
            return token.token

        data = {"sub": str(user.id), "aud": self.token_audience}
        token = self._encode_jwt(
            data, self.secret, self.lifetime_seconds, algorithm=self.algorithm
        )

        Token.create(
            token=token,
            user_id=user.id,
            expire_at=datetime.utcnow() + timedelta(seconds=self.lifetime_seconds),
            created_at=datetime.utcnow(),
        )

        return token

    async def destroy_token(self, token: str, user: models.UserType) -> None:
        token_obj: Optional[Token, None] = Token.get_by_token(token)

        if token_obj is None:
            await token_obj.delete()

            BlacklistedToken.create(
                token=token,
                user_id=user.id,
                expire_at=datetime..utcnow() + timedelta(seconds=self.lifetime_seconds),
                created_at=datetime.utcnow(),
            )
