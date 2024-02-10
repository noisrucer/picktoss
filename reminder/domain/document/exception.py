from fastapi import status

from reminder.core.exception.base import BaseCustomException
from reminder.domain.document.constant import FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM, PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM, DOCUMENT_MAX_LEN


class DocumentNotFoundError(BaseCustomException):
    def __init__(self, document_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Document with id {document_id} is not found")


class FreePlanDocumentUploadLimitExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"무료 플랜 문서 업로드 제한을 초과 했습니다. 무료 플랜은 최대 {FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM}개의 문서를 업로드 할 수 있습니다."
        )

class ProPlanDocumentUploadLimitExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pro 플랜 문서 업로드 제한을 초과 했습니다. 무료 플랜은 최대 {PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM}개의 문서를 업로드 할 수 있습니다."
        )


class DocumentMaxLengthExceedError(BaseCustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"문서 최대 길이 {DOCUMENT_MAX_LEN}를 초과했습니다."
        )