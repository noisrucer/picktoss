from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    member_id: Mapped[str] = mapped_column(String(200), nullable=False)

    # -- relationship

    # ManyToOne / subscription_history(N) : member(1)
    # member = relationship("Member", back_populates="subscriptions", lazy="selectin")
