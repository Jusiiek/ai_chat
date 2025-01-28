from fastapi import Response
from fastapi.security.base import SecurityBase


class AuthResponse:
    scheme: SecurityBase

    @staticmethod
    def get_success_login_response() -> dict: ...

    @staticmethod
    def get_success_logout_response() -> dict: ...

    async def get_login_response(self, token: str) -> Response: ...

    async def get_logout_response(self) -> Response: ...
