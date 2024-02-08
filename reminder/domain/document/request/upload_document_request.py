import json

from pydantic import BaseModel, Field, model_validator

from reminder.domain.document.enum import DocumentFormat


class UploadDocumentRequest(BaseModel):
    userDocumentName: str = Field(default=None, examples=["네트워크 DNS 동작과 원리"])
    categoryId: int = Field(..., examples=[1])
    documentFormat: DocumentFormat = Field(default=DocumentFormat.MARKDOWN, examples=["MARKDOWN"])

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)
