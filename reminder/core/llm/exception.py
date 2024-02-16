from reminder.core.exception.base import BaseCustomException
from fastapi import status


class InvalidLLMJsonResponseError(BaseCustomException):
    llm_response: str

    def __init__(self, llm_response: str):
        self.llm_response = llm_response
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Invalid LLM Response: {llm_response}"
        )
