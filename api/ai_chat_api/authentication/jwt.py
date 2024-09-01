from datetime import timedelta, datetime
from typing import Optional, Union, List, Dict, Any

import jwt
from pydantic import SecretStr

SecretType = Union[str, SecretStr]
JWT_ALGORITHM = "HS256"


def _get_secret_value(secret: SecretType) -> str:
    """
    Return value of a secret.

    returns
    --------
    secret: str - secret value
    """
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


def encode_jwt(
    data: dict,
    secret: SecretType,
    lifetime_seconds: Optional[int] = None,
    algorithm: str = JWT_ALGORITHM,
) -> str:
    """
    Returns JWT encoded jwt.

    Parameters
    ----------
    data : dict - user data to encode
    secret : SecretType - jwt secret
    lifetime_seconds : optional in

    return
    -----------
    token: str - JWT encoded jwt
    """
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    return jwt.encode(payload, _get_secret_value(secret), algorithm=algorithm)


def decode_jwt(
    encoded_jwt: str,
    secret: SecretType,
    audience: List[str],
    algorithms: List[str] = [JWT_ALGORITHM],
) -> Dict[str, Any]:
    """
    Decodes JWT encoded jwt.
    """
    return jwt.decode(
        encoded_jwt,
        _get_secret_value(secret),
        audience=audience,
        algorithms=algorithms
    )
