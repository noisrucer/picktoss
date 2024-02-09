from reminder.domain.question.repository import QuestionRepository
from reminder.domain.question.service import QuestionService
from reminder.domain.document.dependency import document_repository
from reminder.domain.category.dependency import category_repository

question_repository = QuestionRepository()

question_service = QuestionService(
    document_repository=document_repository,
    category_repository=category_repository
)
