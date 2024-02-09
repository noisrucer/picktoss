from fastapi import status

from reminder.core.exception.base import BaseCustomException


class DocumentNotFoundError(BaseCustomException):
    def __init__(self, document_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Document with id {document_id} is not found")
