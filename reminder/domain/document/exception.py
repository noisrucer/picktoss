from fastapi import status

from reminder.core.exception.base import BaseCustomException
from reminder.domain.document.constant import (
    DOCUMENT_MAX_LEN,
    DOCUMENT_MIN_LEN,
    FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM,
    PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM,
    FREE_PLAN_CURRENT_MAX_DOCUMENT_NUM,
    PRO_PLAN_CURRENT_MAX_DOCUMENT_NUM,
)


class DocumentNotFoundError(BaseCustomException):
    def __init__(self, document_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Document with id {document_id} is not found")


class FreePlanCurrentSubscriptionDocumentUploadLimitExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"무료 플랜은 한달에 최대 {FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM}개의 문서를 업로드 할 수 있습니다.",
        )


class ProPlanCurrentSubscriptionDocumentUploadLimitExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pro 플랜은 한달에 최대 {PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM}개의 문서를 업로드 할 수 있습니다.",
        )


class FreePlanAnytimeDocumentUploadLimitExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"무료 플랜은 매 시점 최대 {FREE_PLAN_CURRENT_MAX_DOCUMENT_NUM}개의 문서를 업로드 할 수 있습니다.",
        )


class ProPlanAnytimeDocumentUploadLimitExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pro 플랜은 매 시점 최대 {PRO_PLAN_CURRENT_MAX_DOCUMENT_NUM}개의 문서를 업로드 할 수 있습니다.",
        )


class DocumentMaxLengthExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"문서 최대 길이 {DOCUMENT_MAX_LEN}를 초과했습니다."
        )


class DocumentMinLengthError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"문서 최소 길이는 {DOCUMENT_MIN_LEN}자 입니다."
        )
