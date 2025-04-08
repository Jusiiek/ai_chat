from ai_chat_api.api.models.user import User

USERS_ENDPOINT = "/api/users"


async def test_get_user_success(admin_auth_client, create_test_user):
    test_user: User = create_test_user()

    res = admin_auth_client.get(f"{USERS_ENDPOINT}/{test_user.id}")
    assert res.status_code == 200

    test_user.delete()


async def test_get_user_404(admin_auth_client, create_test_user):
    test_user: User = create_test_user()

    res = admin_auth_client.get(
        f"{USERS_ENDPOINT}/a914015a-73c6-4e55-8e92-f38d0b579122"
    )
    assert res.status_code == 404
    test_user.delete()


async def test_update_user_success(admin_auth_client, create_test_user):
    test_user: User = create_test_user()

    res = admin_auth_client.put(
        f"{USERS_ENDPOINT}/{test_user.id}",
        json={
            "email": "test_user_to_update_and_delete_1@ai_app.com",
        }
    )
    assert res.status_code == 200
    test_user.delete()


async def test_get_me(admin_auth_client):
    res = admin_auth_client.get(f"{USERS_ENDPOINT}/active-user")
    assert res.status_code == 200
