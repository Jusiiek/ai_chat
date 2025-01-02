import uuid
from datetime import datetime
from typing import Optional, Protocol, TypeVar

ID = TypeVar('ID', bound=uuid.UUID)


class UserProtocol(Protocol[ID]):

    id: ID
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    edited_at:  datetime


class AuthProtocol(Protocol[ID]):

    id: ID
    auth_name: str
    access_token: str
    expires_at: Optional[int]
    refresh_token: Optional[str]
    account_id: ID
    account_email: str


UP = TypeVar("UP", bound=UserProtocol)
AP = TypeVar("AP", bound=AuthProtocol)
