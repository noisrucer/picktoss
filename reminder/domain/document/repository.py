from reminder.domain.document.model import Document
from reminder.domain.document.entity import EDocument
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select

class DocumentRepository:

    async def save(self, session: AsyncSession, edocument: EDocument) -> int:
        document = self._to_document(edocument=edocument)
        session.add(document)
        await session.commit()
        return document.id
    
    def sync_find_by_id(self, session: Session, document_id: int) -> Document:
        return session.scalars(select(Document).where(Document.id == document_id)).first()

    def _to_document(self, edocument: EDocument) -> Document:
        return Document(
            format=edocument.format.value,
            s3_key=edocument.s3_key,
            status=edocument.status.value
        )
        

