from typing import TypeVar
from pydantic import BaseModel


class AuthPasswordRequestForm(BaseModel):
    email: str
    password: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str


APRF = TypeVar("APRF", bound=AuthPasswordRequestForm)
ARS = TypeVar("ARS", bound=AuthResponseSchema)
