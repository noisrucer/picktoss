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
    summary: str | None = Field(
        None,
        examples=[
            "DNS 서버는 클라이언트의 조회 메세지를 받아서 회답하는 역할을 한다. 조회 메세지에는 이름, 클래스, 타입 정보가 포함되어 있으며, 이를 기반으로 DNS 서버는 해당 정보에 대한 회답을 찾아서 클라이언트에게 전달한다. DNS 서버에는 A와 MX 이외에도 PTR, CNAME, NS, SOA 등 다양한 타입의 정보를 등록할 수 있으며, 도메인 계층을 따라가며 해당 정보를 찾아내는 방법을 사용한다. DNS 서버는 등록 정보에 유효기간을 설정하고, cache에 저장된 정보의 유효 기간이 지나면 삭제한다."
        ],
    )
    format: str = Field(..., examples=["MARKDOWN"])
    createdAt: datetime = Field(..., examples=["2024-01-01"])
    questions: list[QuestionResponseDto] = Field(...)
    content: str = Field(...)
