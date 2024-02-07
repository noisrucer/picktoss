
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, ForeignKey, Enum, Text
from reminder.core.database.session_manager import Base


class QuestionSet(Base):
    __tablename__ = "question_set"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("document.id"))
    document: Mapped[list] = relationship("Document", back_populates="question_sets")