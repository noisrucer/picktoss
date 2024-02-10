from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from reminder.domain.question.entity import EQuestion
from reminder.domain.question.model import Question, QuestionQuestionSet, QuestionSet


class QuestionRepository:

    def sync_save_all(self, session: Session, questions: list[Question]) -> list[int]:
        for question in questions:
            session.add(question)
        session.commit()
        return [question.id for question in questions]

    def _to_question(self, equestion: EQuestion) -> Question:
        return Question(question=equestion.question, answer=equestion.answer, document_id=equestion.document_id)


class QuestionQuestionSetRepository:
    def sync_save_all(self, session: Session, question_question_sets: list[QuestionQuestionSet]) -> list[int]:
        for question_question_set in question_question_sets:
            session.add(question_question_set)
        session.commit()
        return [qqs.id for qqs in question_question_sets]


class QuestionSetRepository:
    async def find_or_none_by_id(self, session: AsyncSession, question_set_id: str) -> QuestionSet | None:
        query = select(QuestionSet).where(QuestionSet.id == question_set_id)
        result = await session.execute(query)
        return result.scalars().first()

    def sync_save(self, session: Session, question_set: QuestionSet) -> int:
        session.add(question_set)
        session.commit()
        return question_set.id
