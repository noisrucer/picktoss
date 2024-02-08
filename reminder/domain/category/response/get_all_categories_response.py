from pydantic import BaseModel, Field


class CategoryResponseDto(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["네트워크"])


class GetAllCategoriesResponse(BaseModel):
    categories: list[CategoryResponseDto]
