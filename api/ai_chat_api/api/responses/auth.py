from fastapi import Response, status, Header
from fastapi.security.base import SecurityBase
from ai_chat_api.api.common.auth_error import ErrorMessages, ErrorModel


class AuthResponse:
    scheme: SecurityBase

    @staticmethod
    def get_success_login_response() -> dict:
        pass

    @staticmethod
    def get_unsuccessful_login_response() -> dict:
        return {
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorMessages.LOGIN_BAD_CREDENTIALS.value: {
                                "summary": "Bad credentials or the user is inactive.",
                                "value": {
                                    "detail": ErrorMessages.LOGIN_BAD_CREDENTIALS.value
                                },
                            },
                            ErrorMessages.LOGIN_USER_NOT_VERIFIED: {
                                "summary": "The user is not verified.",
                                "value": {
                                    "detail": ErrorMessages.LOGIN_USER_NOT_VERIFIED.value
                                },
                            },
                        }
                    }
                },
            },
        }

    @staticmethod
    def get_success_logout_response() -> dict:
        pass

    @staticmethod
    def get_unsuccessful_register_response() -> dict:
        return {
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorMessages.USER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": (
                                        ErrorMessages.USER_INVALID_PASSWORD.value
                                    )
                                },
                            },
                            ErrorMessages.USER_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": (
                                        ErrorMessages.USER_ALREADY_EXISTS.value
                                    )
                                },
                            },
                        }
                    }
                },
            },
        }

    async def get_login_response(self, token: str) -> Response:
        pass

    async def get_logout_response(self) -> Response:
        pass

    async def get_token_from_request(self, authorization: str = Header(None)) -> str:
        pass
