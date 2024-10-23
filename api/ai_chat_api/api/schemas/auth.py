from typing import Optional, TypeVar
from pydantic import BaseModel


class AuthPasswordRequestForm(BaseModel):
    email: str
    password: str


APRF = TypeVar("APRF", bound=AuthPasswordRequestForm)
