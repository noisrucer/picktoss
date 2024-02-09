from datetime import datetime

from pydantic import BaseModel, Field


class DocumentResponseDto(BaseModel):
    id: int = Field(..., examples=[1])
    documentName: str = Field(..., examples=["네트워크 DNS의 기본 동작"])
    createdAt: datetime = Field(..., examples=[datetime(2024, 4, 4)])


class GetAllDocumentsByCategoryResponse(BaseModel):
    documents: list[DocumentResponseDto]
