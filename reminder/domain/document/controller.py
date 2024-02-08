from fastapi import APIRouter, UploadFile, status

from reminder.dependency.db import DBSessionDep
from reminder.domain.document.dependency import document_service
from reminder.domain.document.entity import EDocument
from reminder.domain.document.request.upload_document_request import (
    UploadDocumentRequest,
)
from reminder.domain.document.response.get_all_documents_by_category_response import GetAllDocumentsByCategoryResponse

router = APIRouter(tags=["post"])


@router.post("/documents", status_code=status.HTTP_200_OK)
async def upload_document(file: UploadFile, request: UploadDocumentRequest, session: DBSessionDep):
    document_name = request.userDocumentName if request.userDocumentName else file.filename
    content_bytes: bytes = await file.read()
    edocument = EDocument(
        name=document_name,
        category_id=request.categoryId,
        content_bytes=content_bytes,
        format=request.documentFormat,
    )

    await document_service.upload_document(session=session, edocument=edocument)
    return {"filename": file.filename}


@router.get("/categories/{category_id}/documents", response_model=GetAllDocumentsByCategoryResponse)
async def get_all_documents_by_category(category_id: int, session: DBSessionDep):
    return await document_service.get_all_documents_by_category(session, category_id)