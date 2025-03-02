import pytest
from fastapi import Response, HTTPException

from ai_chat_api.api.responses.bearer import BearerResponse


def test_get_success_login_response(response: BearerResponse):
    response_dict = response.get_success_login_response()
    assert isinstance(response_dict, dict)


def test_get_success_logout_response(response: BearerResponse):
    response_dict = response.get_success_login_response()
    assert isinstance(response_dict, dict)


@pytest.mark.asyncio
async def test_get_login_response(response: BearerResponse):
    response_dict = await response.get_login_response("random_token")
    assert isinstance(response_dict, Response)


@pytest.mark.asyncio
async def test_get_logout_response(response: BearerResponse):
    response_dict = await response.get_logout_response()
    assert isinstance(response_dict, Response)


@pytest.mark.asyncio
async def test_get_token_from_request_valid(response: BearerResponse):
    auth_header = "Bearer my_test_token"
    token = await response.get_token_from_request(auth_header)
    assert token == "my_test_token"


@pytest.mark.asyncio
async def test_get_token_from_request_missing(response: BearerResponse):
    with pytest.raises(HTTPException) as exc_info:
        await response.get_token_from_request(None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or missing authorization token"
