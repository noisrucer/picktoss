from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reminder.core.database.session_manager import Base
from reminder.shared.base_model import AuditBase
from reminder.domain.subscription.model import Subscription
from reminder.domain.category.model import Category
from reminder.domain.document.model import Document


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


    ## -- Business Logics
    # def is_pro_version(self) -> bool:
    #     subscription_histories: list[Subscription] = self.subscription_histories
    #     if len(subscription_histories) == 0:
    #         return False
        
    #     now = datetime.now()
    #     for subscription_history in subscription_histories:
    #         if now < subscription_history.expire_date:
    #             return True
    #     return False
    
    # def get_num_created_documents(self) -> int:
    #     total_num = 0
    #     categories: list[Category] = self.categories
    #     for category in categories:
    #         documents:
            
        
