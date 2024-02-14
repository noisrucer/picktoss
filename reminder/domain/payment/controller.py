from fastapi import APIRouter, Depends

from reminder.container import payment_repository
from reminder.dependency.db import DBSessionDep
from reminder.domain.member.dependency import get_current_member_id
from reminder.domain.payment.request.create_payment_request import CreatePaymentRequest


router = APIRouter(tags=["Payment"])


@router.post("/payment")
async def request_payment(
    request: CreatePaymentRequest, session: DBSessionDep, member_id: str = Depends(get_current_member_id)
):
    await payment_repository.request_payment(session=session, name=request.name, member_id=member_id)