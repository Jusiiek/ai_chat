from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from ai_chat_api.api.utils.models import model_dump
from ai_chat_api.api.schemas import auth
from ai_chat_api.api.responses.auth import AuthResponse


class BearerResponse(AuthResponse):
    scheme: OAuth2PasswordBearer

    def __init__(self, tokenUrl: str):
        self.scheme = OAuth2PasswordBearer(tokenUrl)

    @staticmethod
    def get_success_login_response() -> dict:
        return {
            status.HTTP_200_OK: {
                "model": auth.ARS,
            }
        }

    @staticmethod
    def get_success_logout_response() -> dict:
        return {}

    async def get_login_response(self, token: str) -> Response:
        bearer_response = auth.ARS(
            access_token=token,
            token_type="bearer",
        )
        return JSONResponse(model_dump(bearer_response))

    async def get_logout_response(self) -> Response:
        raise NotImplementedError()
