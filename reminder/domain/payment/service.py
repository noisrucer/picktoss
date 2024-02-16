from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from reminder.domain.payment.repository import PaymentRepository
from reminder.domain.payment.model import Payment


class PaymentService:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    async def request_payment(self, session: AsyncSession, name: str, member_id: str):
        payment = Payment(name=name, member_id=member_id)

        await self.payment_repository.save(session, payment)
