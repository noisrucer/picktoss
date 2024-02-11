from datetime import datetime

from pydantic import BaseModel, Field

from reminder.domain.subscription.enum import SubscriptionPlanType


class GetScriptionPlanResponse(BaseModel):
    plan: SubscriptionPlanType = Field(..., examples=["PRO"])
    purchased_date: datetime = Field(..., examples=[datetime(2024, 1, 3)])
    expire_date: datetime = Field(..., examples=[datetime(2024, 2, 3)])
