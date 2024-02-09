from sqlalchemy import BigInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.domain.document.model import Document
from reminder.shared.base_model import AuditBase


class Question(Base, AuditBase):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("document.id", ondelete="CASCADE"))

    # -- relationships
    # document: Mapped[Document] = relationship("Document", back_populates="questions", cascade="all")
    document = relationship("Document", back_populates="questions")
