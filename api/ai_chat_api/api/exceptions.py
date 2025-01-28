class AppException(Exception):
    pass


class UserNotExists(AppException):
    pass


class InvalidID(AppException):
    pass


class UserAlreadyExist(AppException):
    pass


class UserInactive(AppException):
    pass


class InvalidVerifyToken(AppException):
    pass


class PasswordInvalid(AppException):
    pass


class NotSupported(AppException):
    pass


class LogoutError(AppException):
    pass


class DestroyTokenError(AppException):
    pass
