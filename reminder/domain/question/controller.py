from fastapi import APIRouter, Depends, status
from reminder.domain.member.dependency import get_current_member_id
from reminder.dependency.db import DBSessionDep
from reminder.domain.question.dependency import question_service
from reminder.domain.question.response.get_all_category_questions_by_document_response import (
    GetAllCategoryQuestionsByDocumentResponse,
)

router = APIRouter(tags=["Question"])


@router.get("/categories/{category_id}/documents/questions", response_model=GetAllCategoryQuestionsByDocumentResponse)
async def get_all_category_questions_by_document(
    category_id: int, session: DBSessionDep, member_id: str = Depends(get_current_member_id)
):
    return await question_service.get_all_category_questions_by_document(session, member_id, category_id)
