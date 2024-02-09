from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from reminder.domain.category.exception import CategoryNotFoundError
from reminder.domain.category.model import Category


class CategoryRepository:
    async def creat_category(self, session: AsyncSession, member_id: int, name: str) -> int:
        category = Category(name=name, member_id=member_id)
        session.add(category)
        await session.commit()
        return category.id

    async def find_all(self, session: AsyncSession, member_id: int) -> list[Category]:
        query = select(Category).where(Category.member_id == member_id)
        result = await session.execute(query)
        return result.scalars().fetchall()

    async def delete_by_id(self, session: AsyncSession, member_id: int, category_id: int) -> None:
        query = delete(Category).where(Category.id == category_id and Category.member_id == member_id)
        res = await session.execute(query)
        await session.commit()

    async def find_or_none_by_id(self, session: AsyncSession, member_id: int, category_id: int) -> Category | None:
        query = select(Category).where(Category.id == category_id and Category.member_id == member_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def update_category_by_id(self, session: AsyncSession, member_id: int, category_id: int, data: dict) -> None:
        query = select(Category).where(Category.id == category_id and Category.member_id == member_id)
        result = await session.execute(query)
        category = result.scalars().first()
        if category is None:
            raise CategoryNotFoundError(category_id)

        for k, v in data.items():
            setattr(category, k, v)

        await session.commit()