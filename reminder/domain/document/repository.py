from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from reminder.domain.category.model import Category
from reminder.domain.document.entity import EDocument
from reminder.domain.document.model import Document, DocumentUpload
from reminder.domain.member.model import Member
from reminder.domain.question.model import Question


class DocumentRepository:

    async def save(self, session: AsyncSession, edocument: EDocument) -> int:
        document = self._to_document(edocument=edocument)
        session.add(document)
        await session.commit()
        return document.id

    async def find_all_by_category_id(self, session: AsyncSession, member_id: str, category_id: int) -> list[Document]:
        query = (
            select(Document)
            .join(Category, Document.category_id == Category.id)
            .join(Member, Category.member_id == Member.id)
            .where(Member.id == member_id)
            .where(Category.id == category_id)
        )
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def find_by_id(self, session: AsyncSession, member_id: str, document_id: int) -> Document | None:
        query = (
            select(Document)
            .join(Category, Document.category_id == Category.id)
            .join(Member, Category.member_id == Member.id)
            .where(Member.id == member_id)
            .where(Document.id == document_id)
        )

        result = await session.execute(query)
        return result.scalars().first()

    async def find_all_by_member_id(self, session: AsyncSession, member_id: str) -> list[Document]:
        query = (
            select(Document)
            .join(Category, Document.category_id == Category.id)
            .join(Member, Category.member_id == Member.id)
            .where(Member.id == member_id)
        )
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
            category_id=edocument.category_id,
        )


class DocumentUploadRepository:

    async def find_all_by_member_id(self, session: AsyncSession, member_id: str) -> list[DocumentUpload]:
        query = select(DocumentUpload).where(DocumentUpload.member_id == member_id)
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def save(self, session: AsyncSession, document_upload: DocumentUpload) -> int:
        session.add(document_upload)
        await session.commit()
        return document_upload.id
