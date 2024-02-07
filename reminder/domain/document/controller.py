from fastapi import APIRouter, Depends, status, UploadFile,File
from reminder.domain.document.request.upload_document_request import UploadDocumentRequest
from reminder.domain.document.entity import EDocument
from reminder.domain.document.dependency import document_service
from reminder.dependency.db import DBSessionDep

router = APIRouter(tags=["post"])


@router.post("/documents", status_code=status.HTTP_200_OK)
async def upload_document(file: UploadFile, request: UploadDocumentRequest, session: DBSessionDep):
    content_bytes: bytes = await file.read()
    edocument = EDocument(
        content_bytes=content_bytes,
        document_name=file.filename,
        user_document_name=request.userDocumentName,
        format=request.documentFormat
    )

    await document_service.upload_document(session=session, edocument=edocument)
    return {"filename": file.filename}
