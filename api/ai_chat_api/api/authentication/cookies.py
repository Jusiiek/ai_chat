from typing import Protocol, Optional

from fastapi.security import APIKeyCookie
from fastapi import Response, status

from ai_chat_api.config import Config

class Cookies(Protocol):
    scheme: APIKeyCookie

    def __init__(
        self,
        cookie_name: str = f"{Config.APP_NAME.lower()}_cookie",
        cookie_age: Optional[int] = None,
        cookie_path: str = "/",
        cookie_secure: bool = True,
        cookie_httponly: bool = True,
    ):
        self.cookie_name = cookie_name
        self.cookie_age = cookie_age
        self.cookie_path = cookie_path
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly

    def _set_cookie(
            self,
            response: Response,
            token: str = ""
    ) -> Response:
        response.set_cookie(
            self.cookie_name,
            token,
            max_age=self.cookie_age,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            path=self.cookie_path,
        )

    def _get_response(self) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def get_login_response(self, token: str) -> Response:
        return self._set_cookie(self._get_response(), token)

    async def get_logout_response(self) -> Response:
        return self._set_cookie(self._get_response())
