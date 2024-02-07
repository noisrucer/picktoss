
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey, Enum
from reminder.core.database.session_manager import Base
from reminder.domain.document.enum import DocumentStatus, DocumentFormat


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    format: Mapped[str] = mapped_column(Enum(DocumentFormat), nullable=False) 
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(Enum(DocumentStatus), nullable=False)