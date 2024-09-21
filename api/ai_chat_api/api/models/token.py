import uuid
from cassandra.cqlengine import columns

from ai_chat_api.api.models.base import BaseModel


class Token(BaseModel):
    __keyspace__ = "token"
    token = columns.Text(primary_key=True)
    user_id = columns.UUID(index=True)
    expire_at = columns.DateTime()
    status = columns.Text(default="")

    @staticmethod
    def create(**kwargs) -> 'Token':
        return Token.create(**kwargs)

    @staticmethod
    def get_by_token(token: str) -> 'Token':
        return Token.get(token)

    @staticmethod
    def get_by_id(token_id: uuid.UUID) -> 'Token':
        return Token.get(id=token_id)

    @classmethod
    def update(cls, **kwargs) -> 'Token':
        return Token.update(**kwargs)

    @classmethod
    def delete(cls) -> None:
        return cls.delete()
