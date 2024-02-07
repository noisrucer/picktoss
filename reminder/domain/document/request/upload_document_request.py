import json

from pydantic import BaseModel, Field, model_validator

from reminder.domain.document.enum import DocumentFormat


class UploadDocumentRequest(BaseModel):
    userDocumentName: str = Field(default="11. 네트워크의 동작과 원리")
    documentFormat: DocumentFormat = Field(default=DocumentFormat.MARKDOWN)

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)
