from fastapi import status

from reminder.core.exception.base import BaseCustomException


class CategoryNotFoundError(BaseCustomException):
    def __init__(self, category_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with id {category_id} is not found")


class DuplicateCategoryNameError(BaseCustomException):
    def __init__(self, name: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with name {name} already exists")
