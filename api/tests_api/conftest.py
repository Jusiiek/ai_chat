import asyncio

import pytest
from fastapi.testclient import TestClient

from ai_chat_api.app import app, startup_event


loop = asyncio.get_event_loop()
loop.run_until_complete(startup_event())
client = TestClient(app)


def get_token(login="test_user@ai_app.com", password="T3stU3sr<>0"):
    res = client.post("/auth/jwt/login", json={"email": login, "password": password})
    assert res.status_code == 200
    data = res.json()
    return f"{data['token_type']} {data['access_token']}"


@pytest.fixture
def auth_client():
    client.headers.update({"Authorization": get_token()})
    return client


@pytest.fixture
def update_delete_client():
    client.headers.update(
        {"Authorization": get_token(
            "test_user_to_update_and_delete@ai_app.com",
            "T3stU3sr<>0"
        )}
    )
    return client


@pytest.fixture
def admin_auth_client():
    client.headers.update(
        {"Authorization": get_token("admin@ai_app.com", "Admin3<>0asd")}
    )
    return client
