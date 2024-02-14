from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from reminder.domain.subscription.enum import SubscriptionPlanType
from reminder.domain.subscription.model import Subscription
from reminder.domain.subscription.repository import SubscriptionRepository
from sqlalchemy.orm import Session


class SubscriptionService:
    def __init__(self, subscription_repository: SubscriptionRepository):
        self.subscription_repository = subscription_repository

    async def get_current_subscription_by_member_id(self, session: AsyncSession, member_id: str) -> Subscription:
        # Get all subscription histories for a ㅈmember
        subscriptions: list[Subscription] = await self.subscription_repository.find_all_by_member_id(session, member_id)

        # Find the latest subscription by purchased_date
        latest_subscription = sorted(subscriptions, key=lambda x: x.purchased_date, reverse=True)[0]

        # Compare the current date and the expire_date. If passed expire_date, create a new FREE subscription.
        now = datetime.utcnow()
        if now > latest_subscription.expire_date:
            mark_expire_date = latest_subscription.expire_date
            while now > mark_expire_date + timedelta(days=30):
                mark_expire_date += timedelta(days=30)

            latest_subscription = Subscription(
                plan_type=SubscriptionPlanType.FREE,
                purchased_date=mark_expire_date,
                expire_date=mark_expire_date + timedelta(days=30),
                member_id=member_id,
            )

            await self.subscription_repository.save(session, latest_subscription)

        return latest_subscription
    
    def sync_get_current_subscription_by_member_id(self, session: Session, member_id: str) -> Subscription:
        # Get all subscription histories for a member
        subscriptions: list[Subscription] = self.subscription_repository.sync_find_all_by_member_id(session, member_id)

        # Find the latest subscription by purchased_date
        latest_subscription = sorted(subscriptions, key=lambda x: x.purchased_date, reverse=True)[0]

        # Compare the current date and the expire_date. If passed expire_date, create a new FREE subscription.
        now = datetime.utcnow()
        if now > latest_subscription.expire_date:
            mark_expire_date = latest_subscription.expire_date
            while now > mark_expire_date + timedelta(days=30):
                mark_expire_date += timedelta(days=30)

            latest_subscription = Subscription(
                plan_type=SubscriptionPlanType.FREE,
                purchased_date=mark_expire_date,
                expire_date=mark_expire_date + timedelta(days=30),
                member_id=member_id,
            )

            self.subscription_repository.sync_save(session, latest_subscription)

        return latest_subscription

