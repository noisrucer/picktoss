from dataclasses import dataclass


@dataclass
class EQuestion:
    question: str
    answer: str
    document_id: int
