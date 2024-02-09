from pydantic import BaseModel, Field


class CreateCategoryResponse(BaseModel):
    id: int = Field(..., examples=[1])
