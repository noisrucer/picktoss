from fastapi import APIRouter, Depends, Form, UploadFile, status

from reminder.dependency.db import DBSessionDep
from reminder.domain.document.dependency import document_service
from reminder.domain.document.entity import EDocument
from reminder.domain.document.enum import DocumentFormat
from reminder.domain.document.response.get_all_documents_by_category_response import (
    GetAllDocumentsByCategoryResponse,
)
from reminder.domain.document.response.get_document_response import GetDocumentResponse
from reminder.domain.document.response.upload_document_response import (
    UploadDocumentResponse,
)
from reminder.domain.member.dependency import get_current_member_id

router = APIRouter(tags=["Document"])


@router.post("/documents", status_code=status.HTTP_200_OK, response_model=UploadDocumentResponse)
async def upload_document(
    file: UploadFile,
    session: DBSessionDep,
    userDocumentName: str = Form(default=None),
    categoryId: str = Form(...),
    documentFormat: DocumentFormat = Form(...),
    member_id: str = Depends(get_current_member_id),
):
    document_name = userDocumentName if userDocumentName else file.filename
    content_bytes: bytes = await file.read()
    edocument = EDocument(
        name=document_name,
        category_id=categoryId,
        content_bytes=content_bytes,
        format=documentFormat,
    )

    return await document_service.upload_document(session=session, member_id=member_id, edocument=edocument)


@router.get("/categories/{category_id}/documents", response_model=GetAllDocumentsByCategoryResponse)
async def get_all_documents_by_category(
    category_id: int, session: DBSessionDep, member_id: str = Depends(get_current_member_id)
):
    return await document_service.get_all_documents_by_category(session, member_id, category_id)


@router.get("/documents/{document_id}", response_model=GetDocumentResponse)
async def get_document(document_id: int, session: DBSessionDep, member_id: str = Depends(get_current_member_id)):
    return await document_service.get_document_by_id(session, member_id, document_id)
