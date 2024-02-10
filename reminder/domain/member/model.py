from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.shared.base_model import AuditBase


class Member(Base, AuditBase):
    __tablename__ = "member"

    id: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)
    # pro_version: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # pro_version_purchased_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # def is_pro_version(self) -> bool:
    #     return self.pro_version
    

    ## -- relationships
    categories = relationship("Category", back_populates="member", cascade="all, delete-orphan")
