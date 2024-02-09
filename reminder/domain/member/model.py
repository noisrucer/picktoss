from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.shared.base_model import AuditBase


class Member(Base, AuditBase):
    __tablename__ = "member"

    id: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)

    ## -- relationships

    # OneToMany / member(1) : category(N)
    # categories = relationship("Category", cascade="all, delete", backref="member")

    ## - new relationships
    categories = relationship("Category", back_populates="member", cascade="all, delete-orphan")