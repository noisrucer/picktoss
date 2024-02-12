from sqlalchemy.ext.asyncio.session import AsyncSession

from reminder.domain.category.exception import CategoryNotFoundError, DuplicateCategoryNameError
from reminder.domain.category.model import Category
from reminder.domain.category.repository import CategoryRepository
from reminder.domain.category.response.create_category_response import (
    CreateCategoryResponse,
)
from reminder.domain.category.response.get_all_categories_response import (
    CategoryResponseDto,
    GetAllCategoriesResponse,
)


class CategoryService:
    def __init__(self, category_repostiory: CategoryRepository):
        self.category_repostiory = category_repostiory

    async def create_category(self, session: AsyncSession, member_id: str, name: str) -> CreateCategoryResponse:
        # Check duplicating category name
        category = await self.category_repostiory.find_or_none_by_name(session, member_id, name)
        if category:
            raise DuplicateCategoryNameError(name)

        category_id = await self.category_repostiory.creat_category(session, member_id, name)
        return CreateCategoryResponse(id=category_id)

    async def find_all_categories(self, session: AsyncSession, member_id: str) -> GetAllCategoriesResponse:
        categories: list[Category] = await self.category_repostiory.find_all(session, member_id)
        return GetAllCategoriesResponse(
            categories=[CategoryResponseDto(id=category.id, name=category.name) for category in categories]
        )

    async def delete_category_by_id(self, session: AsyncSession, member_id: str, category_id: int) -> None:
        # 2. Delete category
        await self.category_repostiory.delete_by_id(session, member_id, category_id)

    async def update_category_by_id(
        self, session: AsyncSession, member_id: str, category_id: int, new_name: str
    ) -> None:
        await self.category_repostiory.update_category_by_id(session, member_id, category_id, {"name": new_name})
