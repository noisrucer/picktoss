from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from reminder.domain.document.entity import EDocument
from reminder.domain.document.model import Document


class DocumentRepository:

    async def save(self, session: AsyncSession, edocument: EDocument) -> int:
        document = self._to_document(edocument=edocument)
        session.add(document)
        await session.commit()
        return document.id
    
    async def find_all_by_category_id(self, session: AsyncSession, category_id: int) -> list[Document]:
        query = select(Document).where(Document.category_id == category_id)
        result = await session.execute(query)
        return result.scalars().fetchall()

    def sync_find_by_id(self, session: Session, document_id: int) -> Document:
        return session.scalars(select(Document).where(Document.id == document_id)).first()

    def _to_document(self, edocument: EDocument) -> Document:
        return Document(
            name=edocument.name,
            format=edocument.format.value,
            s3_key=edocument.s3_key,
            status=edocument.status.value,
            category_id=edocument.category_id
        )
