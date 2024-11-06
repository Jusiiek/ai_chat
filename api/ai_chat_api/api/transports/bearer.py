from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from ai_chat_api.api.protocols.security_transport import SecurityTransport
from ai_chat_api.api.schemas.user import model_dump
from ai_chat_api.api.exceptions import NotSupported


class BearerResponseSchema(BaseModel):
    access_token: str
    token_type: str


class BearerTransport(SecurityTransport):
    scheme: OAuth2PasswordBearer

    def __init__(self, tokenUrl: str):
        self.token_url = OAuth2PasswordBearer(tokenUrl, auto_error=False)

    async def get_login_response(self, token: str) -> Response:
        bearer_response = BearerResponseSchema(
            access_token=token,
            token_type="bearer",
        )
        return JSONResponse(model_dump(bearer_response))

    async def get_logout_response(self) -> Response:
        raise NotSupported()

    @staticmethod
    def get_success_login_response() -> dict:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponseSchema,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "some0token",
                            "token_type": "bearer",
                        }
                    }
                }
            }
        }

    @staticmethod
    def get_success_logout_response() -> dict:
        return {}
