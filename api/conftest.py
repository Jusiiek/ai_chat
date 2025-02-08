import asyncio

from fastapi.testclient import TestClient

from ai_chat_api.app import app, startup_event


loop = asyncio.get_event_loop()
loop.run_until_complete(startup_event())
client = TestClient(app)


def get_token(login="test_user@test.com", password="T3st@test.com"):
    res = client.post("/auth/jwt/login", data={"username": login, "password": password})
    assert res.status_code == 200
    data = res.json()
    return f"{data['token_type']} {data['access_token']}"


def get_auth_client():
    client.headers.update({"Authorization": get_token()})
    return client
