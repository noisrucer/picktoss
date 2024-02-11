from fastapi import APIRouter, Depends, status

from reminder.dependency.db import DBSessionDep
from reminder.domain.member.dependency import get_current_member_id
from reminder.domain.subscription.model import Subscription
from reminder.domain.subscription.response.get_subscription_plan_response import (
    GetScriptionPlanResponse,
)

router = APIRouter(tags=["Subscription"])


# @router.get("/subscription-plan", response_model=GetScriptionPlanResponse)
# async def get_subscription_plan(session: DBSessionDep, member_id: str = Depends(get_current_member_id)) -> GetScriptionPlanResponse:
#     subscription: Subscription = await subsription_service.get_current_subscription_by_member_id(session, member_id)
#     return GetScriptionPlanResponse(
#         plan=subscription.plan_type,
#         purchased_date=subscription.purchased_date,
#         expire_date=subscription.expire_date
#     )
