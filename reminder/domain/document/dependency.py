from reminder.core.llm.openai import chat_llm
from reminder.dependency.core import s3_client, sqs_client
from reminder.domain.category.dependency import category_repository
from reminder.domain.document.repository import DocumentRepository, DocumentUploadRepository
from reminder.domain.document.service import DocumentService
from reminder.domain.member.dependency import member_repository
from reminder.domain.subscription.dependency import subsription_service

document_repository = DocumentRepository()
document_upload_repository = DocumentUploadRepository()

document_service = DocumentService(
    document_repository=document_repository,
    document_upload_repository=document_upload_repository,
    category_repository=category_repository,
    member_repository=member_repository,
    subscription_service=subsription_service,
    chat_llm=chat_llm,
    s3_client=s3_client,
    sqs_client=sqs_client,
)
