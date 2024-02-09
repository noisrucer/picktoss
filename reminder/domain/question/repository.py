from sqlalchemy.orm import Session

from reminder.domain.question.entity import EQuestion
from reminder.domain.question.model import Question


class QuestionRepository:

    def sync_save_all(self, session: Session, equestions: list[EQuestion]) -> list[int]:
        questions = [self._to_question(equestion) for equestion in equestions]
        for question in questions:
            session.add(question)
        session.commit()
        return [question.id for question in questions]

    def _to_question(self, equestion: EQuestion) -> Question:
        return Question(question=equestion.question, answer=equestion.answer, document_id=equestion.document_id)
