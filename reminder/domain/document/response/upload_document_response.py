from pydantic import BaseModel, Field


class UploadDocumentResponse(BaseModel):
    id: int = Field(..., examples=[1])