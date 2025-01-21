from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from ai_chat_api.api.schemas.user import model_dump
from ai_chat_api.api.schemas import auth


class AuthResponse:
    scheme: OAuth2PasswordBearer

    def __init__(self, token_url: str):
        self.token_url = OAuth2PasswordBearer(token_url, auto_error=False)

    async def get_login_response(self, token: str) -> Response:
        bearer_response = auth.ARS(
            access_token=token,
            token_type="bearer",
        )
        return JSONResponse(model_dump(bearer_response))

    async def get_logout_response(self) -> Response:
        raise NotImplementedError()

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
