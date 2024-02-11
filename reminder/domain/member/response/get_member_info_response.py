from datetime import datetime

from pydantic import BaseModel, Field

from reminder.domain.subscription.enum import SubscriptionPlanType


class GetMemberInfoSubScriptionDto(BaseModel):
    plan: SubscriptionPlanType = Field(..., examples=["PRO"])
    purchasedDate: datetime = Field(..., examples=[datetime(2024, 1, 3)])
    expireDate: datetime = Field(..., examples=[datetime(2024, 2, 3)])


class GetMemberInfoDocumentDto(BaseModel):
    currentSubscriptionCycleTotalDocuments: int = Field(..., examples=[15])
    currentSubscriptionCycleUsedDocuments: int = Field(..., examples=[7])


class GetMemberInfoResponse(BaseModel):
    subscription: GetMemberInfoSubScriptionDto = Field(...)
    document: GetMemberInfoDocumentDto = Field(...)
