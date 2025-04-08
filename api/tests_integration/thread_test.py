from ai_chat_api.api.models.user import User

THREADS_ENDPOINT = "/api/threads"


def test_create_thread_success(admin_auth_client):
    res = admin_auth_client.post(
        f"{THREADS_ENDPOINT}/",
        json={
            "user_message": "Test user message"
        }
    )
    assert res.status_code == 200


def test_get_user_threads_success(admin_auth_client):
    res = admin_auth_client.get(
        f"{THREADS_ENDPOINT}/",
    )
    assert res.status_code == 200


def test_get_thread_success(admin_auth_client, create_test_user, create_test_thread):
    test_user: User = create_test_user()
    test_thread = create_test_thread(test_user.id)

    res = admin_auth_client.get(
        f"{THREADS_ENDPOINT}/{test_thread.id}",
    )
    assert res.status_code == 200
    test_user.delete()
    test_thread.delete()
