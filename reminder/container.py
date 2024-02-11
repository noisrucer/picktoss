from reminder.domain.member.repository import MemberRepository
from reminder.domain.member.service import MemberService

from reminder.domain.category.repository import CategoryRepository
from reminder.domain.category.service import CategoryService

from reminder.core.llm.openai import chat_llm
from reminder.dependency.core import s3_client, sqs_client
from reminder.domain.document.repository import DocumentRepository, DocumentUploadRepository
from reminder.domain.document.service import DocumentService

from reminder.domain.question.repository import QuestionRepository, QuestionQuestionSetRepository, QuestionSetRepository
from reminder.domain.question.service import QuestionService

from reminder.domain.subscription.service import SubscriptionService
from reminder.domain.subscription.repository import SubscriptionRepository


subscription_repository = SubscriptionRepository()
category_repository = CategoryRepository()
question_repository = QuestionRepository()
question_set_repository = QuestionSetRepository()
question_question_set_repository = QuestionQuestionSetRepository()
document_repository = DocumentRepository()
document_upload_repository = DocumentUploadRepository()
member_repository = MemberRepository()

subscription_service = SubscriptionService(subscription_repository=subscription_repository)
question_service = QuestionService(
    document_repository=document_repository,
    category_repository=category_repository,
    question_set_repository=question_set_repository,
)

document_service = DocumentService(
    document_repository=document_repository,
    document_upload_repository=document_upload_repository,
    category_repository=category_repository,
    member_repository=member_repository,
    subscription_service=subscription_service,
    chat_llm=chat_llm,
    s3_client=s3_client,
    sqs_client=sqs_client,
)

category_service = CategoryService(category_repository)

member_service = MemberService(
    member_repository=member_repository,
    subscription_repository=subscription_repository,
    subscription_service=subscription_service,
    document_service=document_service
)
