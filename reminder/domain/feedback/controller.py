from fastapi import APIRouter, Depends

from reminder.container import feedback_service
from reminder.dependency.db import DBSessionDep
from reminder.domain.member.dependency import get_current_member_id
from reminder.domain.feedback.request.create_feedback_request import CreateFeedbackRequest


router = APIRouter(tags=["Feedback"])


@router.post("/feedback")
async def receive_feedback(
    request: CreateFeedbackRequest, session: DBSessionDep, member_id: str = Depends(get_current_member_id)
):
    await feedback_service.receive_feedback(session=session, content=request.content, member_id=member_id)
