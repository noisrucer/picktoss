from datetime import datetime

from fastapi import APIRouter, Depends, status

from reminder.dependency.db import DBSessionDep
from reminder.domain.member.dependency import get_current_member_id

# from reminder.domain.question.dependency import question_service
from reminder.container import question_service
from reminder.domain.question.response.get_all_category_questions_by_document_response import (
    GetAllCategoryQuestionsByDocumentResponse,
)
from reminder.domain.question.response.get_question_set_by_id_response import (
    GetQuestionSetByIdResponse,
)
from reminder.domain.question.response.get_question_set_today_response import (
    GetQuestionSetTodayResponse,
)

router = APIRouter(tags=["Question"])


@router.get("/categories/{category_id}/documents/questions", response_model=GetAllCategoryQuestionsByDocumentResponse)
async def get_all_category_questions_by_document(
    category_id: int, session: DBSessionDep, member_id: str = Depends(get_current_member_id)
):
    return await question_service.get_all_category_questions_by_document(session, member_id, category_id)


@router.get("/question-sets/today", response_model=GetQuestionSetTodayResponse)
async def get_question_set_today(session: DBSessionDep, member_id: str = Depends(get_current_member_id)):
    return await question_service.get_question_set_today(session, member_id)


@router.get("/question-sets/{question_set_id}", response_model=GetQuestionSetByIdResponse)
async def get_question_set(question_set_id: str, session: DBSessionDep):
    return await question_service.get_question_set_by_id(session, question_set_id)
