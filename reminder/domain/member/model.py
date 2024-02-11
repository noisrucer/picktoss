from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.domain.category.model import Category
from reminder.domain.document.model import Document
from reminder.domain.subscription.model import Subscription
from reminder.shared.base_model import AuditBase


class Member(Base, AuditBase):
    __tablename__ = "member"

    id: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)

    ## -- relationships

    # OneToMany / member(1) : category(N)
    categories = relationship("Category", back_populates="member", cascade="all, delete-orphan", lazy="selectin")

    # OneToMany / member(1) : subscription_history(N)
    subscriptions = relationship("Subscription", back_populates="member", cascade="all, delete-orphan", lazy="selectin")
