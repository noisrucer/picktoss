from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.shared.base_model import AuditBase
from reminder.domain.subscription.enum import SubscriptionPlanType


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, index=True)
    plan_type: Mapped[SubscriptionPlanType] = mapped_column(Enum(SubscriptionPlanType), nullable=False)
    purchased_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expire_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    member_id: Mapped[str] = mapped_column(String(200), ForeignKey("member.id", ondelete="CASCADE"), nullable=False)

    # -- relationship

    # ManyToOne / subscription_history(N) : member(1)
    member = relationship("Member", back_populates="subscriptions", lazy="selectin")
