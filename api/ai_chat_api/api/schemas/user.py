from typing import Optional, TypeVar
from pydantic import BaseModel

from ai_chat_api.api.protocols import models


class CreateUpdateModel(BaseModel):
    def create_update_dict(self):
        return self.model_dump(
            self,
            exclude_unset=True,
            exclude={"id"}
        )


class BaseUser(CreateUpdateModel):
    """ Base User model """

    id: models.ID
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class BaseCreateUser(CreateUpdateModel):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class BaseUpdateUser(CreateUpdateModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class BaseAuthModel(BaseModel):
    """ Base Auth Model """

    id: models.ID
    auth_name: str
    access_token: str
    expires_at: Optional[int]
    refresh_token: Optional[str]
    account_id: models.ID
    account_email: str


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=BaseCreateUser)
UU = TypeVar("UU", bound=BaseUpdateUser)
