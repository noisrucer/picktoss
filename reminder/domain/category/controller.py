from fastapi import APIRouter, Depends, status

from reminder.dependency.db import DBSessionDep

# from reminder.domain.category.dependency import category_service
from reminder.container import category_service
from reminder.domain.category.request.create_category_request import (
    CreateCategoryRequest,
)
from reminder.domain.category.request.update_category_request import (
    UpdateCategoryRequest,
)
from reminder.domain.category.response.create_category_response import (
    CreateCategoryResponse,
)
from reminder.domain.category.response.get_all_categories_response import (
    GetAllCategoriesResponse,
)
from reminder.domain.member.dependency import get_current_member_id

router = APIRouter(tags=["Category"])

@router.get("/hello", status_code=status.HTTP_200_OK)
async def hello():
    return {"hello": hello}

@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=CreateCategoryResponse)
async def create_category(
    request: CreateCategoryRequest, session: DBSessionDep, member_id: str = Depends(get_current_member_id)
):
    return await category_service.create_category(session, member_id, request.name)


@router.get("/categories", status_code=status.HTTP_200_OK, response_model=GetAllCategoriesResponse)
async def get_all_categories(session: DBSessionDep, member_id: str = Depends(get_current_member_id)):
    return await category_service.find_all_categories(session, member_id)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(session: DBSessionDep, category_id: int, member_id: str = Depends(get_current_member_id)):
    await category_service.delete_category_by_id(session, member_id, category_id)


@router.patch("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(
    session: DBSessionDep,
    category_id: int,
    request: UpdateCategoryRequest,
    member_id: str = Depends(get_current_member_id),
):
    await category_service.update_category_by_id(session, member_id, category_id, request.newName)
