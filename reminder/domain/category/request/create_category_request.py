from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    name: str = Field(default=..., examples=["네트워크"])
