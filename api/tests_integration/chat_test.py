from ai_chat_api.api.models.user import User
from ai_chat_api.api.models.chat import Chat

CHATS_ENDPOINT = "/api/chats"


def create_test_chat(thread_id, user_id):
    return Chat.create(
        thread_id=thread_id,
        user_id=user_id,
    )


def test_get_chat(admin_auth_client, create_test_user, create_test_thread):
    test_user: User = create_test_user()
    test_thread = create_test_thread(test_user.id)
    test_chat = create_test_chat(test_thread.id, test_user.id)

    res = admin_auth_client.get(
        f"{CHATS_ENDPOINT}/{test_chat.id}",
    )
    assert res.status_code == 200

    test_user.delete()
    test_thread.delete()
    test_chat.delete()


def test_create_chat(admin_auth_client, create_test_user, create_test_thread):
    test_user: User = create_test_user()
    test_thread = create_test_thread(test_user.id)

    res = admin_auth_client.post(
        f"{CHATS_ENDPOINT}/{test_thread.id}",
        json={"user_message": "test user message"}
    )
    assert res.status_code == 200

    test_user.delete()
    test_thread.delete()
