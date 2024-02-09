from sqlalchemy.ext.asyncio.session import AsyncSession
from reminder.domain.document.repository import DocumentRepository
from reminder.domain.question.response.get_all_category_questions_by_document_response import GetAllCategoryQuestionsByDocumentResponse, DocumentResponseDto, QuestionResponseDto
from reminder.domain.category.repository import CategoryRepository
from reminder.domain.category.exception import CategoryNotFoundError

class QuestionService:
    def __init__(
            self,
            document_repository: DocumentRepository,
            category_repository: CategoryRepository
    ):
        self.document_repository = document_repository
        self.category_repository = category_repository
    
    async def get_all_category_questions_by_document(
            self, session: AsyncSession, member_id: str, category_id: int
    ) -> GetAllCategoryQuestionsByDocumentResponse:
        category = await self.category_repository.find_or_none_by_id(session, member_id, category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        
        documents = await self.document_repository.find_all_by_category_id(session, member_id, category_id)
        return GetAllCategoryQuestionsByDocumentResponse(
            documents=[
                DocumentResponseDto(
                    id=doc.id,
                    documentName=doc.name,
                    createdAt=doc.created_at,
                    questions=[QuestionResponseDto(id=question.id, question=question.question, answer=question.answer) for question in doc.questions if question.delivered_count > 0]
                )
                for doc in documents
            ]
        )
