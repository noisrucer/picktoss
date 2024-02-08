
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String

from reminder.core.database.session_manager import Base


class Member(Base):
    __tablename__ = "member"

    # id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)