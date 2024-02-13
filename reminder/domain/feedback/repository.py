from sqlalchemy.ext.asyncio import AsyncSession
from reminder.domain.feedback.model import Feedback


class FeedbackRepository:

    async def save(self, session: AsyncSession, feedback: Feedback) -> int:
        session.add(feedback)
        await session.commit()
        return feedback.id
