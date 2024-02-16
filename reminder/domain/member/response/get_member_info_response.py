from datetime import datetime

from pydantic import BaseModel, Field

from reminder.domain.subscription.enum import SubscriptionPlanType


class GetMemberInfoSubScriptionDto(BaseModel):
    plan: SubscriptionPlanType = Field(..., examples=["PRO"])
    purchasedDate: datetime = Field(..., examples=[datetime(2024, 1, 3)])
    expireDate: datetime = Field(..., examples=[datetime(2024, 2, 3)])


class GetMemberInfoDocumentDto(BaseModel):
    # 현재
    currentPossessDocumentNum: int = Field(..., examples=[7], description="현재 업로드 된 문서 개수")
    currentSubscriptionCycleUploadedDocumentNum: int = Field(
        ..., examples=[36], description="현재 구독 기간 동안 업로드한 문서 개수"
    )

    # Free
    freePlanMaxPossessDocumentNum: int = Field(..., examples=[7], description="Free 플랜 최대 문서 보유 개수")
    freePlanSubscriptionMaxUploadDocumentNum: int = Field(
        ..., examples=[30], description="Free 플랜 구독 기간 최대 업로드 문서 개수"
    )

    # Pro
    proPlanMaxPossessDocumentNum: int = Field(..., examples=[20], description="Pro 플랜 최대 문서 보유 개수")
    proPlanSubscriptionMaxUploadDocumentNum: int = Field(
        ..., examples=[50], description="Pro 플랜 구독 기간 최대 업로드 문서 개수"
    )


class GetMemberInfoQuizDto(BaseModel):
    freePlanQuizQuestionNum: int = Field(..., examples=[3])
    proPlanQuizQuestionNum: int = Field(..., examples=[10])


class GetMemberInfoResponse(BaseModel):
    email: str = Field(..., examples=["changjin9792@gmail.com"])
    subscription: GetMemberInfoSubScriptionDto = Field(...)
    documentUsage: GetMemberInfoDocumentDto = Field(...)
    quiz: GetMemberInfoQuizDto = Field(...)
