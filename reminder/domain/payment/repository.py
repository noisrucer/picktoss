from sqlalchemy.ext.asyncio import AsyncSession
from reminder.domain.payment.model import Payment


class PaymentRepository:

    async def save(self, session: AsyncSession, payment: Payment) -> int:
        session.add(payment)
        await session.commit()
        return payment.id
