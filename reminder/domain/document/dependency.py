from reminder.domain.document.service import DocumentService
from reminder.domain.document.repository import DocumentRepository
from reminder.core.llm.openai import chat_llm
from reminder.dependency.core import s3_client

document_repository = DocumentRepository()

document_service = DocumentService(
    document_repository=document_repository,
    chat_llm=chat_llm,
    s3_client=s3_client
)