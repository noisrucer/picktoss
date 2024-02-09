import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession

from reminder.core.llm.openai import OpenAIChatLLM
from reminder.core.s3.s3_client import S3Client
from reminder.core.sqs.sqs_client import SQSClient
from reminder.domain.category.exception import CategoryNotFoundError
from reminder.domain.category.repository import CategoryRepository
from reminder.domain.document.entity import EDocument
from reminder.domain.document.exception import DocumentNotFoundError
from reminder.domain.document.model import Document
from reminder.domain.document.repository import DocumentRepository
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


class DocumentService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        category_repository: CategoryRepository,
        chat_llm: OpenAIChatLLM,
        s3_client: S3Client,
        sqs_client: SQSClient,
    ):
        self.document_repository = document_repository
        self.category_repository = category_repository
        self.chat_llm = chat_llm
        self.s3_client = s3_client
        self.sqs_client = sqs_client

    async def upload_document(
        self, session: AsyncSession, member_id: str, edocument: EDocument
    ) -> UploadDocumentResponse:
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

        # 3. Send a message to SQS for Lambda LLM worker to consume
        self.sqs_client.put({"s3_key": s3_key, "db_pk": document_id})

        return UploadDocumentResponse(id=document_id)

    async def get_all_documents_by_category(
        self, session: AsyncSession, member_id: str, category_id: int
    ) -> GetAllDocumentsByCategoryResponse:
        category = await self.category_repository.find_or_none_by_id(session, member_id, category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)

        documents: list[Document] = await self.document_repository.find_all_by_category_id(session, member_id, category_id)
        return GetAllDocumentsByCategoryResponse(
            documents=[
                DocumentResponseDto(id=document.id, documentName=document.name, createdAt=document.created_at)
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
            format=document.format,
            createdAt=document.created_at,
            questions=[QuestionResponseDto(id=q.id, question=q.question, answer=q.answer) for q in document.questions if q.delivered_count > 0],
            content=content,
        )
