from datetime import datetime

from pydantic import BaseModel, Field

from reminder.domain.document.enum import DocumentStatus


class QuestionResponseDto(BaseModel):
    id: int = Field(..., examples=[10])
    question: str = Field(..., examples=["네트워크가 뭔가요?"])
    answer: str = Field(..., examples=["저도 모릅니다"])


class CategoryResponseDto(BaseModel):
    id: int = Field(..., examples=[15])
    name: str = Field(..., examples=["네트워크"])


class GetDocumentResponse(BaseModel):
    id: int = Field(..., examples=[1])
    status: DocumentStatus = Field(..., examples=[DocumentStatus.UNPROCESSED])
    category: CategoryResponseDto
    documentName: str = Field(..., examples=["네트워크 DNS의 기본과 원리"])
    format: str = Field(..., examples=["MARKDOWN"])
    createdAt: datetime = Field(..., examples=["2024-01-01"])
    questions: list[QuestionResponseDto] = Field(...)
    content: str = Field(...)
