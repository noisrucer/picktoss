from reminder.domain.document.repository import DocumentRepository
from reminder.domain.document.entity import EDocument
from reminder.core.llm.openai import OpenAIChatLLM
from reminder.core.llm.utils import load_prompt_messages, fill_message_placeholders
from reminder.core.s3.s3_client import S3Client
from reminder.core.sqs.sqs_client import SQSClient
import uuid
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

class DocumentService:
    def __init__(self, document_repository: DocumentRepository, chat_llm: OpenAIChatLLM, s3_client: S3Client, sqs_client: SQSClient):
        self.document_repository = document_repository
        self.chat_llm = chat_llm
        self.s3_client = s3_client
        self.sqs_client = sqs_client

    async def upload_document(self, session: AsyncSession, edocument: EDocument) -> int:
        # 1. Upload document to S3
        s3_key = uuid.uuid4().hex
        self.s3_client.upload_bytes_obj(
            obj_bytes=edocument.content_bytes,
            key=s3_key,
            metadata={"format": edocument.format.value}
        )
        edocument.assign_s3_key(s3_key)

        # 2. Save to DB
        document_id = await self.document_repository.save(session, edocument)

        # 3. Send a message to SQS so that Lambda LLM worker can consume
        self.sqs_client.put({"s3_key": s3_key, "db_pk": document_id})

        

