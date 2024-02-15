from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.domain.document.model import Document
from reminder.shared.base_model import AuditBase


class Question(Base, AuditBase):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    delivered_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("document.id", ondelete="CASCADE"), nullable=False)
    # document_id: Mapped[int] = mapped_column(BigInteger, nullable=False) # manage FK at application level?

    # -- relationships

    # ManyToOne / Question(N) : Document(1)
    document = relationship("Document", back_populates="questions", lazy="selectin", foreign_keys=[document_id])

    # OneToMany / Question(1) : QuestionQuestionSet(N)
    question_question_sets = relationship("QuestionQuestionSet", back_populates="question", cascade="all, delete-orphan", lazy="selectin")


class QuestionQuestionSet(Base, AuditBase):
    __tablename__ = "question_question_set"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    question_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("question.id", ondelete="CASCADE"))  # ManyToOne
    # question_set_id: Mapped[str] = mapped_column(String(300))  # ManyToOne
    question_set_id: Mapped[str] = mapped_column(String(300), ForeignKey("question_set.id", ondelete="CASCADE"))  # ManyToOne

    # -- relationships

    # ManyToOne / (QuestionQuestionSet(N) : Question(1))
    question = relationship("Question", back_populates="question_question_sets", lazy="selectin")

    # ManyToOne / (QuestionQuestionSet(N) : QuestionSet(1))
    question_set = relationship("QuestionSet", back_populates="question_question_sets", lazy="selectin")


class QuestionSet(Base, AuditBase):
    __tablename__ = "question_set"

    id: Mapped[str] = mapped_column(String(300), primary_key=True, index=True)
    member_id: Mapped[str] = mapped_column(String(100), ForeignKey("member.id"))

    # -- relationships

    # OneToMany / QuestionSet(1) : QuestionQuestionSet(N)
    question_question_sets = relationship("QuestionQuestionSet", back_populates="question_set", lazy="selectin")
