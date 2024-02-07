from reminder.domain.document.model import Document
from reminder.domain.document.entity import EDocument
from sqlalchemy.ext.asyncio import AsyncSession

class DocumentRepository:

    async def save(self, session: AsyncSession, edocument: EDocument) -> int:
        document = self._to_document(edocument=edocument)
        session.add(document)
        await session.commit()
        return document.id

    def _to_document(self, edocument: EDocument) -> Document:
        return Document(
            format=edocument.format.value,
            s3_key=edocument.s3_key,
            status=edocument.status.value
        )
        