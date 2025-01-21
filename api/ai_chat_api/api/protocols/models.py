import uuid
from typing import TypeVar
from pydantic import BaseModel


ID = TypeVar("ID", bound=uuid.UUID)
UserType = TypeVar('UserType', bound=BaseModel)
