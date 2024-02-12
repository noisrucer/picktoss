from datetime import datetime

from pydantic import BaseModel, Field

from reminder.domain.subscription.enum import SubscriptionPlanType


class GetMemberInfoSubScriptionDto(BaseModel):
    plan: SubscriptionPlanType = Field(..., examples=["PRO"])
    purchasedDate: datetime = Field(..., examples=[datetime(2024, 1, 3)])
    expireDate: datetime = Field(..., examples=[datetime(2024, 2, 3)])


class GetMemberInfoDocumentDto(BaseModel):
    currentSubscriptionCycleMaxDocumentNum: int = Field(..., examples=[45], description="구독 기간 동안 업로드 할 수 있는 총 문서 개수")
    currentSubscriptionCycleUploadedDocumentNum: int = Field(..., examples=[36], description="현재 구독 기간 동안 업로드한 문서 개수")
    anytimeMaxDocumentNum: int = Field(..., examples=[15], description="매 시점 업로드 될 수 있는 최대 문서 개수.")
    currentUploadedDocumentNum: int = Field(..., examples=[7], description="현재 업로드 된 문서 개수")


class GetMemberInfoResponse(BaseModel):
    email: str = Field(..., examples=["changjin9792@gmail.com"])
    subscription: GetMemberInfoSubScriptionDto = Field(...)
    documentUsage: GetMemberInfoDocumentDto = Field(...)
