from typing import Optional
from pydantic import BaseModel

from ai_chat_api.api.protocols import models


class CreateUpdateModel(BaseModel):
    class Config:
        from_attributes = True

    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={"id"}
        )


class BaseUser(CreateUpdateModel):
    """ Base User model """

    id: models.ID
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class BaseCreateUser(CreateUpdateModel):
    """ Base User creation model """

    email: str
    password: str
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class BaseUpdateUser(CreateUpdateModel):
    """ Base User update model """

    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
