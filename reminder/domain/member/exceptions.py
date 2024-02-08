from fastapi import status

from reminder.core.exception.base import BaseCustomException


class JWTError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "JWT error"
        

class InvalidTokenScopeError(BaseCustomException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect token scope"