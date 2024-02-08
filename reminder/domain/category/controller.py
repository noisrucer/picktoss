from fastapi import APIRouter, status
from reminder.domain.category.request.create_category_request import CreateCategoryRequest 
from reminder.domain.category.response.create_category_response import CreateCategoryResponse
from reminder.domain.category.response.get_all_categories_response import GetAllCategoriesResponse
from reminder.dependency.db import DBSessionDep
from reminder.domain.category.dependency import category_service
from reminder.domain.category.request.update_category_request import UpdateCategoryRequest

router = APIRouter(tags=["Category"])


@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=CreateCategoryResponse)
async def create_category(request: CreateCategoryRequest, session: DBSessionDep):
    return await category_service.create_category(session, request.name)


@router.get("/categories", status_code=status.HTTP_200_OK, response_model=GetAllCategoriesResponse)
async def get_all_categories(session: DBSessionDep):
    return await category_service.find_all_categories(session)

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(session: DBSessionDep, category_id: int):
    await category_service.delete_category_by_id(session, category_id)

@router.patch("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(session: DBSessionDep, category_id: int, request: UpdateCategoryRequest):
    await category_service.update_category_by_id(session, category_id, request.newName)