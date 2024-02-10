from fastapi import status

from reminder.core.exception.base import BaseCustomException


class QuestionSetNotFoundError(BaseCustomException):
    def __init__(self, question_set_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Question set with id {question_set_id} is not found")
