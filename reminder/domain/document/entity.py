from dataclasses import dataclass

from reminder.domain.document.enum import DocumentFormat, DocumentStatus


@dataclass
class EDocument:
    name: str
    category_id: int
    content_bytes: bytes
    format: DocumentFormat
    s3_key: str | None = None
    status: DocumentStatus = DocumentStatus.UNPROCESSED

    def decode_contenet_str(self) -> str:
        return self.content_bytes.decode("utf-8")

    def assign_s3_key(self, s3_key: str) -> None:
        self.s3_key = s3_key
