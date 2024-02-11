from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from reminder.domain.subscription.model import Subscription


class SubscriptionRepository:

    async def find_all_by_member_id(self, session: AsyncSession, member_id: str) -> list[Subscription]:
        query = select(Subscription).where(Subscription.member_id == member_id)
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def save(self, session: AsyncSession, subscription: Subscription) -> int:
        session.add(subscription)
        await session.commit()
        return subscription.id
    
    def sync_find_all_by_member_id(self, session: Session, member_id: str) -> list[Subscription]:
        query = select(Subscription).where(Subscription.member_id == member_id)
        result = session.execute(query)
        return result.scalars().fetchall()
    
    def sync_save(self, session: Session, subscription: Subscription) -> int:
        session.add(subscription)
        session.commit()
        return subscription.id
