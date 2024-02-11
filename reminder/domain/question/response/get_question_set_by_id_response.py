from datetime import datetime

from pydantic import BaseModel, Field


class GetQuestionSetByIdDocumentDto(BaseModel):
    id: int = Field(..., examples=[229])
    name: str = Field(..., examples=["네트워크 DNS 동작과 원리"])


class GetQuestionSetByIdCategoryDto(BaseModel):
    id: int = Field(..., examples=[83])
    name: str = Field(..., examples=["네트워크"])


class GetQuestionSetByIdQuestionDto(BaseModel):
    id: int = Field(..., examples=[10])
    question: str = Field(..., examples=["네트워크가 뭔가요?"])
    answer: str = Field(..., examples=["저도 모릅니다"])
    category: GetQuestionSetByIdCategoryDto = Field(...)
    document: GetQuestionSetByIdDocumentDto = Field(...)


class GetQuestionSetByIdResponse(BaseModel):
    questions: list[GetQuestionSetByIdQuestionDto] = Field(...)
