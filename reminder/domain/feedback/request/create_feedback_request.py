from pydantic import BaseModel, Field


class CreateFeedbackRequest(BaseModel):
    content: str = Field(default=...)
