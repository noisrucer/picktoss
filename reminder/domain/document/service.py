from reminder.domain.document.repository import DocumentRepository
from reminder.domain.document.entity import EDocument, QuestionSet
from reminder.core.llm.openai import OpenAIChatLLM
from reminder.core.llm.utils import load_prompt_messages, fill_message_placeholders
from reminder.core.s3.s3_client import S3Client
import uuid
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

class DocumentService:
    def __init__(self, document_repository: DocumentRepository, chat_llm: OpenAIChatLLM, s3_client: S3Client):
        self.document_repository = document_repository
        self.chat_llm = chat_llm
        self.s3_client = s3_client

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


        # 3. Send a message to SQS

        # content = edocument.content
        # CHUNK_SIZE = 2000
        # chunks = []
        # for i in range(0, len(content), CHUNK_SIZE):
        #     # if len(content) - i < 500:
        #     #     continue
        #     chunks.append(content[i: i + CHUNK_SIZE])

        # # 1. Generate questions from the content
        # question_sets: list[QuestionSet] = []
        # for chunk in chunks:
        #     messages = load_prompt_messages(self.generate_questions_prompt_path)
        #     messages = fill_message_placeholders(
        #         messages=messages,
        #         placeholders={"note": chunk}
        #     )
        #     resp_dict = await self.chat_llm.apredict_json(messages=messages)
            
        #     for q_set in resp_dict:
        #         question, answer = q_set['question'], q_set['answer']
        #         question_set = QuestionSet(question, answer)
        #         question_sets.append(question_set)
        #         print(f"Question: {question}")
        #         print(f"Answer: {answer}")
        #         print("-" * 100)
        #     break

        # 2. Upload to S3

        # 3. Save document, questions to DB


