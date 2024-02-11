from pydantic import BaseModel, Field


class GetQuestionSetTodayResponse(BaseModel):
    questionSetId: str | None = Field(None, examples=["sjsdf998z7987899xz"])
    message: str | None = Field(None, examples=["DOCUMENT_NOT_CREATED_YET", "QUESTION_SET_NOT_READY"])
