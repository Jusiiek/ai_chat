from enum import Enum
from typing import List

from ai_chat_api.api.models.base import BaseModel


class PasswordErrorMessages(str, Enum):
    PASSWORD_MISSING_UPPERCASE = "PASSWORD_MISSING_UPPERCASE"
    PASSWORD_MISSING_LOWERCASE = "PASSWORD_MISSING_LOWERCASE"
    PASSWORD_MISSING_DIGIT = "PASSWORD_MISSING_DIGIT"
    PASSWORD_MISSING_SPECIAL_CHAR = "PASSWORD_MISSING_SPECIAL_CHARACTER"
    PASSWORD_TOO_SHORT = "PASSWORD_TOO_SHORT"


class PasswordErrorsHolder:
    def __init__(self, password: str, errors: List[str], is_valid: bool):
        self.password = password
        self.errors = errors
        self.is_valid = is_valid
