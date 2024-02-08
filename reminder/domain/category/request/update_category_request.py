from pydantic import BaseModel, Field


class UpdateCategoryRequest(BaseModel):
    newName: str = Field(..., examples = ["someNewName"])