from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime
from reminder.core.database.session_manager import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from reminder.shared.base_model import AuditBase


class Category(Base, AuditBase):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    # created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # -- relationships

    # OneToMany
    documents = relationship(
        "Document", cascade="all, delete", backref="category"
    )