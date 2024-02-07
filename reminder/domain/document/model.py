from sqlalchemy import BigInteger, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.domain.document.enum import DocumentFormat, DocumentStatus
from reminder.domain.question_set.model import QuestionSet


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    format: Mapped[str] = mapped_column(Enum(DocumentFormat), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(Enum(DocumentStatus), nullable=False)

    question_sets: Mapped[list[QuestionSet]] = relationship(
        "QuestionSet", back_populates="document", cascade="all, delete-orphan"
    )

    def complete_process(self):
        self.status = DocumentStatus.PROCESSED
