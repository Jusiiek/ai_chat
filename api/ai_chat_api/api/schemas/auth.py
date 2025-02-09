from typing import TypeVar
from pydantic import BaseModel
from fastapi import Form
from typing_extensions import Annotated, Doc


class AuthPasswordRequestForm(BaseModel):
    email: str
    password: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str


APRF = TypeVar("APRF", bound=AuthPasswordRequestForm)
ARS = TypeVar("ARS", bound=AuthResponseSchema)


class AuthRequestForm:
    def __init__(
        self,
        email: Annotated[
            str,
            Form(),
            Doc(
                """
                `email` string. The OAuth2 spec requires the exact field name
                `email`.
                """
            ),
        ],
        password: Annotated[
            str,
            Form(),
            Doc(
                """
                `password` string. The OAuth2 spec requires the exact field name
                `password".
                """
            ),
        ]
    ):
        self.email = email
        self.password = password
