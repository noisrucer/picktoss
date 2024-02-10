from sqlalchemy.ext.asyncio import AsyncSession
from reminder.domain.subscription.model import Subscription
from sqlalchemy import select


class SubscriptionRepository:
    
    async def find_all_by_member_id(self, session: AsyncSession, member_id: str) -> list[Subscription]:
        query = select(Subscription).where(Subscription.member_id == member_id)
        result = await session.execute(query)
        return result.scalars().fetchall()
    
    async def save(self, session: AsyncSession, subscription: Subscription) -> int:
        session.add(subscription)
        await session.commit()
        return subscription.id
