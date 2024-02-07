from dataclasses import dataclass


@dataclass
class EQuestionSet:
    question: str
    answer: str
    document_id: int
