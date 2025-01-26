from fastapi import Response
from fastapi.security.base import SecurityBase


class AuthResponse:
    scheme: SecurityBase

    @staticmethod
    def success_login_response() -> dict: ...

    @staticmethod
    def success_logout_response() -> dict: ...

    async def login_response(self, token: str) -> Response: ...

    async def logout_response(self) -> Response: ...
