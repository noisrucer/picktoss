from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from reminder.domain.feedback.repository import FeedbackRepository
from reminder.domain.feedback.model import Feedback

class FeedbackService:
    def __init__(self, feedback_repository: FeedbackRepository):
        self.feedback_repository = feedback_repository
        
    
    async def receive_feedback(self, session: AsyncSession, content: str, member_id: str):
        feedback = Feedback(
            content=content,
            member_id=member_id
        )
        
        await self.feedback_repository.save(session, feedback)