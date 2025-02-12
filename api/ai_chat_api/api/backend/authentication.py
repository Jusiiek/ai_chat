from fastapi import Response, status

from ai_chat_api.api.managers.token import TokenManager
from ai_chat_api.api.responses.auth import AuthResponse
from ai_chat_api.api.models.user import User
from ai_chat_api.api import exceptions


class AuthenticationBackend:
    """
    The AuthenticationBackend instance.
    Provides authentication logic such as login and logout details.

    Args
    -------------
    responses: AuthResponse - Authentication responses instance.
    token_manager: TokenManager - Token manager instance.
    """

    responses: AuthResponse
    token_manager: TokenManager

    def __init__(self, responses: AuthResponse, token_manager: TokenManager):
        self.responses = responses
        self.token_manager = token_manager

    async def login(self, user: User) -> Response:
        """
        Writes token for the user and returns successful login response.

        Args
        -----------
        user: User - User instance.

        Returns
        -----------
        response: Response - Successful login response.
        """
        token = await self.token_manager.write_token(user)
        return await self.responses.get_login_response(token)

    async def logout(self, token: str, user: User) -> Response:
        """
        Destroys the user's token and returns successful logout response.

        Args
        -----------
        token: str - token to destroy.
        user: User - User instance.

        Returns
        -----------
        response: Response - Successful logout response.
        """
        try:
            await self.token_manager.destroy_token(token, user)
            response = await self.responses.get_logout_response()
        except exceptions.DestroyTokenError:
            response = Response(status_code=status.HTTP_204_NO_CONTENT)

        return response
