from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy.sql import func

from reminder.core.database.session_manager import Base
from reminder.domain.category.model import Category
from reminder.domain.document.enum import DocumentFormat, DocumentStatus
from reminder.shared.base_model import AuditBase


class Document(Base, AuditBase):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    format: Mapped[str] = mapped_column(Enum(DocumentFormat), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(Enum(DocumentStatus), nullable=False)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    # -- relationships

    # ManyToOne / document(N) : category(1)
    category = relationship("Category", back_populates="documents", lazy="selectin")

    # OneToMany / document(1): question(N)
    questions = relationship("Question", back_populates="document", cascade="all, delete-orphan", lazy="selectin")

    document_upload = relationship(
        "DocumentUpload", back_populates="document", cascade="all, delete-orphan", lazy="selectin"
    )

    def complete_process(self):
        self.status = DocumentStatus.PROCESSED


class DocumentUpload(Base):
    __tablename__ = "document_upload"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    upload_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    # N:1
    member_id: Mapped[str] = mapped_column(String(200), ForeignKey("member.id", ondelete="CASCADE"), nullable=False)
    document_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("document.id", ondelete="CASCADE"), nullable=False)

    ## -- relationship
    document = relationship("Document", back_populates="document_upload", lazy="selectin")
