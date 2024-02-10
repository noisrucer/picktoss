from sqlalchemy.ext.asyncio.session import AsyncSession
from reminder.domain.document.repository import DocumentRepository
from reminder.domain.question.response.get_all_category_questions_by_document_response import (
    GetAllCategoryQuestionsByDocumentResponse,
    DocumentResponseDto,
    QuestionResponseDto,
)
from reminder.domain.category.repository import CategoryRepository
from reminder.domain.category.exception import CategoryNotFoundError
from reminder.domain.question.repository import QuestionSetRepository
from reminder.domain.question.exception import QuestionSetNotFoundError
from reminder.domain.question.response.get_question_set_by_id_response import GetQuestionSetByIdResponse, GetQuestionSetByIdDocumentDto, GetQuestionSetByIdCategoryDto, GetQuestionSetByIdQuestionDto
from reminder.domain.question.model import QuestionQuestionSet, Question, QuestionSet
from reminder.domain.document.model import Document
from reminder.domain.category.model import Category


class QuestionService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        category_repository: CategoryRepository,
        question_set_repository: QuestionSetRepository
    ):
        self.document_repository = document_repository
        self.category_repository = category_repository
        self.question_set_repository = question_set_repository

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
                    summary=doc.summary,
                    createdAt=doc.created_at,
                    questions=[
                        QuestionResponseDto(id=question.id, question=question.question, answer=question.answer)
                        for question in doc.questions
                        if question.delivered_count > 0
                    ],
                )
                for doc in documents
            ]
        )
    
    async def get_question_set_by_id(
        self, session: AsyncSession, question_set_id: str
    ) -> GetQuestionSetByIdResponse:
        question_set = await self.question_set_repository.find_or_none_by_id(session, question_set_id)
        if question_set is None:
            raise QuestionSetNotFoundError(question_set_id)
        
        question_question_sets: list[QuestionQuestionSet] = question_set.question_question_sets

        question_dtos: list[GetQuestionSetByIdQuestionDto] = []
        for qqs in question_question_sets:
            question: Question = qqs.question
            document: Document = question.document
            category: Category = document.category
            
            category_dto = GetQuestionSetByIdCategoryDto(id=category.id, name=category.name)
            document_dto = GetQuestionSetByIdDocumentDto(id=document.id, name=document.name)

            question_dto = GetQuestionSetByIdQuestionDto(
                id=question.id,
                question=question.question,
                answer=question.answer,
                category=category_dto,
                document=document_dto
            )

            question_dtos.append(question_dto)
        
        return GetQuestionSetByIdResponse(questions=question_dtos)



