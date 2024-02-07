from dataclasses import dataclass
from reminder.domain.document.enum import DocumentStatus, DocumentFormat


@dataclass
class EDocument:
    content_bytes: bytes
    document_name: str
    user_document_name: str
    format: DocumentFormat
    s3_key: str | None = None
    status: DocumentStatus = DocumentStatus.UNPROCESSED

    def decode_contenet_str(self) -> str:
        return self.content_bytes.decode("utf-8")
    
    def assign_s3_key(self, s3_key: str) -> None:
        self.s3_key = s3_key
