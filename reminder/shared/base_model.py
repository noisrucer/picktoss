from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime
from reminder.core.database.session_manager import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class AuditBase:
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())