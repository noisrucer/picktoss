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


class MemberNotFoundError(BaseCustomException):
    def __init__(self, member_id: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Member with id {member_id} is not found"
