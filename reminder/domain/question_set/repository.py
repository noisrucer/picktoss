from sqlalchemy.orm import Session
from reminder.domain.question_set.model import QuestionSet
from reminder.domain.question_set.entity import EQuestionSet

class QuestionSetRepository:

    def sync_save_all(self, session: Session, equestion_sets: list[EQuestionSet]) -> list[int]:
        question_sets = [self._to_question_set(equestion_set) for equestion_set in equestion_sets]
        for question_set in question_sets:
            session.add(question_set)
        session.commit()
        return [question_set.id for question_set in question_sets]

    def _to_question_set(self, equestion_set: EQuestionSet) -> QuestionSet:
        return QuestionSet(
            question=equestion_set.question,
            answer=equestion_set.answer,
            document_id=equestion_set.document_id
        )
    