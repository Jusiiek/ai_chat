class AppException(Exception):
    pass

class UserNotExist(AppException):
    pass

class UserAlreadyExist(AppException):
    pass

class UserInactive(AppException):
    pass

class InvalidVerifyToken(AppException):
    pass