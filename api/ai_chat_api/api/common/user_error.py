from enum import Enum


class UserErrorMessages(str, Enum):
    USER_DOES_NOT_EXIST = "USER_DOES_NOT_EXIST"
    NOT_A_SUPERUSER = "NOT_A_SUPERUSER"
