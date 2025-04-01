class AppException(Exception):
    pass


class UserNotExists(AppException):
    def __init__(self):
        message = "User doesn't exist"
        super().__init__(message)


class DoesNotExist(AppException):
    def __init__(self):
        message = "Object doesn't exist"
        super().__init__(message)


class InvalidID(AppException):
    pass


class UserAlreadyExists(AppException):
    pass


class UserInactive(AppException):
    pass


class InvalidVerifyToken(AppException):
    pass


class PasswordInvalid(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotSupported(AppException):
    pass


class LogoutError(AppException):
    pass


class DestroyTokenError(AppException):
    pass
