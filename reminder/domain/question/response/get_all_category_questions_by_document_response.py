from datetime import datetime
from pydantic import BaseModel, Field


class QuestionResponseDto(BaseModel):
    id: int = Field(..., examples=[10])
    question: str = Field(..., examples=["네트워크가 뭔가요?"])
    answer: str = Field(..., examples=["저도 모릅니다"])


class DocumentResponseDto(BaseModel):
    id: int = Field(..., examples=[1])
    documentName: str = Field(..., examples=["네트워크 DNS 동작과 원리"])
    createdAt: datetime = Field(..., examples=[datetime(2024, 11, 5)])
    questions: list[QuestionResponseDto] = Field(...)


class GetAllCategoryQuestionsByDocumentResponse(BaseModel):
    documents: list[DocumentResponseDto]