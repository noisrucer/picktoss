from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from reminder.core.database.session_manager import Base
from reminder.shared.base_model import AuditBase


class Category(Base, AuditBase):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    member_id: Mapped[int] = mapped_column(String(100), ForeignKey("member.id", ondelete="CASCADE"))

    # -- relationships

    # OneToMany
    # documents = relationship("Document", cascade="all, delete", backref="category")
    member = relationship("Member", back_populates="categories")

    # -- new relationships
    documents = relationship("Document", back_populates="category", cascade="all, delete-orphan")
