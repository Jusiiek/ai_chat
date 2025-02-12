from fastapi import Response, status, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from ai_chat_api.api.utils.models import model_dump
from ai_chat_api.api.schemas.auth import AuthResponseSchema
from ai_chat_api.api.responses.auth import AuthResponse
from ai_chat_api.api.common.auth_error import ErrorMessages, ErrorModel


class BearerResponse(AuthResponse):
    scheme: OAuth2PasswordBearer

    def __init__(self, tokenUrl: str):
        self.scheme = OAuth2PasswordBearer(tokenUrl)

    @staticmethod
    def get_success_login_response() -> dict:
        return {
            status.HTTP_200_OK: {
                "model": AuthResponseSchema,
            }
        }

    @staticmethod
    def get_success_logout_response() -> dict:
        return {
            status.HTTP_401_UNAUTHORIZED: {
                "model": ErrorModel,
                "description": ErrorMessages.UNAUTHORIZED.value,
            }
        }

    async def get_login_response(self, token: str) -> Response:
        bearer_response = AuthResponseSchema(
            access_token=token,
            token_type="Bearer",
        )
        return JSONResponse(model_dump(bearer_response))

    async def get_logout_response(self) -> Response:
        return JSONResponse(
            status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.UNAUTHORIZED.value
        )

    async def get_token_from_request(self, authorization: str = Header(None)) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Invalid or missing authorization token"
            )
        return authorization[len("Bearer "):]
