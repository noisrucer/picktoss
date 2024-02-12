from fastapi import status

from reminder.core.exception.base import BaseCustomException


class JWTError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT Error"
        )


class InvalidTokenScopeError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token scope"
        )


class MemberNotFoundError(BaseCustomException):
    def __init__(self, member_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member with id {member_id} is not found"
        )
