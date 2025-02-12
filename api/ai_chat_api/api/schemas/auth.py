from pydantic import BaseModel


class AuthPasswordRequestForm(BaseModel):
    email: str
    password: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str
