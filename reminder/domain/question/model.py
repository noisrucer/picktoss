from sqlalchemy import BigInteger, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.domain.document.model import Document
from reminder.shared.base_model import AuditBase


class Question(Base, AuditBase):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    delivered_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("document.id", ondelete="CASCADE"))

    # -- relationships
    document = relationship("Document", back_populates="questions")
