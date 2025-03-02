USERS_ENDPOINT = "/users"


def test_get_me(auth_client):
    res = auth_client.get(f"{USERS_ENDPOINT}/me")
    assert res.status_code == 200


def test_update_me(auth_client):
    res = auth_client.put(f"{USERS_ENDPOINT}/me", json={"password": "T3stU3sr<<<0"})
    assert res.status_code == 200


def test_update_and_delete_user(update_delete_client, admin_auth_client):
    res = update_delete_client.get(f"{USERS_ENDPOINT}/me")
    assert res.status_code == 200
    data = res.json()
    user_id = data["id"]

    update_res = admin_auth_client.put(
        f"{USERS_ENDPOINT}/{user_id}",
        json={"is_active": True, "is_verified": True}
    )
    data = update_res.json()
    assert update_res.status_code == 200
    assert data["is_active"] is True
    assert data["is_verified"] is True

    delete_res = admin_auth_client.delete(f"{USERS_ENDPOINT}/{user_id}")
    assert delete_res.status_code == 204
