import asyncio

import pytest
from fastapi.testclient import TestClient

from ai_chat_api.app import app, startup_event
from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.thread import Thread


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
def admin_auth_client():
    client.headers.update(
        {"Authorization": get_token("admin@ai_app.com", "Admin3<>0asd")}
    )
    return client


@pytest.fixture
def create_test_user():

    def create_user():
        return User.create(
            email="test_user_to_update_and_delete@ai_app.com",
            hashed_password="T3stU3sr<>0",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
    return create_user


@pytest.fixture
def create_test_thread():
    def create_thread(user_id):
        return Thread.create(
            user_id=user_id,
            title="test thread title"
        )
    return create_thread
