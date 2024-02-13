from pydantic import BaseModel, Field


class CreatePaymentRequest(BaseModel):
    name: str = Field(default=..., examples=["홍길동"])
