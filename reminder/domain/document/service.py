import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession

from reminder.core.llm.openai import OpenAIChatLLM
from reminder.core.s3.s3_client import S3Client
from reminder.core.sqs.sqs_client import SQSClient
from reminder.domain.category.exception import CategoryNotFoundError
from reminder.domain.category.repository import CategoryRepository
from reminder.domain.document.constant import (
    DOCUMENT_MAX_LEN,
    DOCUMENT_MIN_LEN,
    FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM,
    PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM,
    FREE_PLAN_CURRENT_MAX_DOCUMENT_NUM,
    PRO_PLAN_CURRENT_MAX_DOCUMENT_NUM,
)
from reminder.domain.document.entity import EDocument
from reminder.domain.document.enum import DocumentStatus
from reminder.domain.document.exception import (
    DocumentMaxLengthExceedError,
    DocumentMinLengthError,
    DocumentNotFoundError,
    FreePlanCurrentSubscriptionDocumentUploadLimitExceedError,
    ProPlanCurrentSubscriptionDocumentUploadLimitExceedError,
    FreePlanAnytimeDocumentUploadLimitExceedError,
    ProPlanAnytimeDocumentUploadLimitExceedError,
)
from reminder.domain.document.model import Document, DocumentUpload
from reminder.domain.document.repository import (
    DocumentRepository,
    DocumentUploadRepository,
)
from reminder.domain.document.response.get_all_documents_by_category_response import (
    DocumentResponseDto,
    GetAllDocumentsByCategoryResponse,
)
from reminder.domain.document.response.get_document_response import (
    CategoryResponseDto,
    GetDocumentResponse,
    QuestionResponseDto,
)
from reminder.domain.document.response.upload_document_response import (
    UploadDocumentResponse,
)
from reminder.domain.member.repository import MemberRepository
from reminder.domain.subscription.enum import SubscriptionPlanType
from reminder.domain.subscription.model import Subscription
from reminder.domain.subscription.service import SubscriptionService


class DocumentService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        document_upload_repository: DocumentUploadRepository,
        category_repository: CategoryRepository,
        member_repository: MemberRepository,
        subscription_service: SubscriptionService,
        chat_llm: OpenAIChatLLM,
        s3_client: S3Client,
        sqs_client: SQSClient,
    ):
        self.document_repository = document_repository
        self.document_upload_repository = document_upload_repository
        self.category_repository = category_repository
        self.member_repository = member_repository
        self.subscription_service = subscription_service
        self.chat_llm = chat_llm
        self.s3_client = s3_client
        self.sqs_client = sqs_client

    async def upload_document(
        self, session: AsyncSession, member_id: str, edocument: EDocument
    ) -> UploadDocumentResponse:
        # Ensure subscription plan document limit
        current_subscription: Subscription = await self.subscription_service.get_current_subscription_by_member_id(
            session, member_id
        )

        # 현재 시점에 업로드된 문서 개수: (제한 - Free: 3개, Pro: 15개)
        current_num_uploaded_documents: int = await self.get_num_current_uploaded_documents_by_member_id(
            session, member_id
        )

        # 현재 구독 사이클에 업로드한 문서 개수: (제한 - Free: 15개, Pro: 40개)
        current_subscription_num_uploaded_documents: int = (
            await self.get_num_uploaded_documents_for_current_subscription_by_member_id(session, member_id)
        )
        plan_type: SubscriptionPlanType = current_subscription.plan_type

        assert isinstance(plan_type, SubscriptionPlanType)
        if plan_type == SubscriptionPlanType.FREE:
            if current_subscription_num_uploaded_documents >= FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM:  # 15개
                raise FreePlanCurrentSubscriptionDocumentUploadLimitExceedError()
            if current_num_uploaded_documents >= FREE_PLAN_CURRENT_MAX_DOCUMENT_NUM:  # 매 시점: 3개
                raise FreePlanAnytimeDocumentUploadLimitExceedError()
        elif plan_type == SubscriptionPlanType.PRO:
            if current_subscription_num_uploaded_documents >= PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM:  # 40개
                raise ProPlanCurrentSubscriptionDocumentUploadLimitExceedError()
            if current_num_uploaded_documents >= PRO_PLAN_CURRENT_MAX_DOCUMENT_NUM:  # 매 시점: 15개
                raise ProPlanAnytimeDocumentUploadLimitExceedError()
        else:
            raise ValueError("Invalid Plan Type")

        # Ensure document max size limit (15,000 characters)
        if len(edocument.decode_contenet_str()) > DOCUMENT_MAX_LEN:
            raise DocumentMaxLengthExceedError()

        if len(edocument.decode_contenet_str()) < DOCUMENT_MIN_LEN:
            raise DocumentMinLengthError()

        # Ensure Category exists
        category_id = edocument.category_id
        category = await self.category_repository.find_or_none_by_id(session, member_id, category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)

        # 1. Upload document to S3
        s3_key = uuid.uuid4().hex
        self.s3_client.upload_bytes_obj(
            obj_bytes=edocument.content_bytes, key=s3_key, metadata={"format": edocument.format.value}
        )
        edocument.assign_s3_key(s3_key)

        # 2. Save to DB
        document_id = await self.document_repository.save(session, edocument)

        document_upload = DocumentUpload(member_id=member_id, document_id=document_id)
        document_upload_id = await self.document_upload_repository.save(session, document_upload)

        # 3. Send a message to SQS for Lambda LLM worker to consume
        self.sqs_client.put({"s3_key": s3_key, "db_pk": document_id, "subscription_plan": str(plan_type.value)})

        return UploadDocumentResponse(id=document_id)

    async def get_all_documents_by_category(
        self, session: AsyncSession, member_id: str, category_id: int
    ) -> GetAllDocumentsByCategoryResponse:
        category = await self.category_repository.find_or_none_by_id(session, member_id, category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)

        documents: list[Document] = await self.document_repository.find_all_by_category_id(
            session, member_id, category_id
        )
        return GetAllDocumentsByCategoryResponse(
            documents=[
                DocumentResponseDto(
                    id=document.id,
                    documentName=document.name,
                    status= DocumentStatus.PROCESSED 
                    if document.status == DocumentStatus.PARTIAL_SUCCESS 
                    or document.status == DocumentStatus.PROCESSED 
                    else DocumentStatus.UNPROCESSED,
                    summary=document.summary,
                    createdAt=document.created_at,
                )
                for document in documents
            ]
        )

    async def get_document_by_id(self, session: AsyncSession, member_id: str, document_id: int) -> GetDocumentResponse:
        document = await self.document_repository.find_by_id(session, member_id, document_id)
        if document is None:
            raise DocumentNotFoundError(document_id)

        s3_key = document.s3_key
        bucket_obj = self.s3_client.get_object(s3_key)
        content = bucket_obj.decode_content_str()

        return GetDocumentResponse(
            id=document.id,
            status=document.status,
            category=CategoryResponseDto(id=document.category.id, name=document.category.name),
            documentName=document.name,
            summary=document.summary,
            format=document.format,
            createdAt=document.created_at,
            questions=[
                QuestionResponseDto(id=q.id, question=q.question, answer=q.answer)
                for q in document.questions
                if q.delivered_count > 0
            ],
            content=content,
        )

    async def delete_document_by_id(self, session: AsyncSession, member_id: str, document_id: int) -> None:
        await self.document_repository.delete_by_member_id_and_id(session, member_id, document_id)

    async def get_num_uploaded_documents_for_current_subscription_by_member_id(
        self, session: AsyncSession, member_id: str
    ) -> int:
        current_subscription: Subscription = await self.subscription_service.get_current_subscription_by_member_id(
            session, member_id
        )
        purchased_date = current_subscription.purchased_date
        expire_date = current_subscription.expire_date

        # Retrieve all document uploads
        document_uploads = await self.document_upload_repository.find_all_by_member_id(session, member_id)

        # Filter by [purchased_date, expire_date] of the current subscription.
        current_subscription_document_uploads = [
            doc for doc in document_uploads if doc.upload_date >= purchased_date and doc.upload_date < expire_date
        ]

        return len(current_subscription_document_uploads)

    async def get_num_current_uploaded_documents_by_member_id(self, session: AsyncSession, member_id: str) -> int:
        """현재 업로드된 문서 개수"""
        documents = await self.document_repository.find_all_by_member_id(session, member_id)
        return len(documents)
