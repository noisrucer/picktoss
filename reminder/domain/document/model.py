from sqlalchemy import BigInteger, Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from reminder.core.database.session_manager import Base
from reminder.domain.document.enum import DocumentFormat, DocumentStatus
from reminder.domain.category.model import Category
from reminder.shared.base_model import AuditBase

class Document(Base, AuditBase):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    format: Mapped[str] = mapped_column(Enum(DocumentFormat), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(Enum(DocumentStatus), nullable=False)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    
    # -- relationships
    
    # ManyToOne / document(N) : category(1)
    # category: Mapped[Category] = relationship(Category, backref=backref("documents", cascade="all, delete-orphan"))

    # OneToMany / document(1): question(N)
    questions = relationship(
        "Question", cascade="all, delete", backref="document"
    )

    def complete_process(self):
        self.status = DocumentStatus.PROCESSED
