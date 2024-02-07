import enum

class DocumentStatus(enum.Enum):
    UNPROCESSED = "UNPROCESSED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class DocumentFormat(enum.Enum):
    MARKDOWN = "MARKDOWN"
    PDF = "PDF"