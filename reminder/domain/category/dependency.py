from reminder.domain.category.repository import CategoryRepository
from reminder.domain.category.service import CategoryService

category_repository = CategoryRepository()

category_service = CategoryService(category_repository)