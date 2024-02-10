from reminder.domain.question.repository import QuestionRepository, QuestionQuestionSetRepository, QuestionSetRepository
from reminder.domain.question.service import QuestionService
from reminder.domain.document.dependency import document_repository
from reminder.domain.category.dependency import category_repository

question_repository = QuestionRepository()
question_set_repository = QuestionSetRepository()
question_question_set_repository = QuestionQuestionSetRepository()

question_service = QuestionService(document_repository=document_repository, category_repository=category_repository, question_set_repository=question_set_repository)
