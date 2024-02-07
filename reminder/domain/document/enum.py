import enum

class DocumentStatus(enum.Enum):
    UNPROCESSED = "UNPROCESSED"
    PROCESSED = "PROCESSED"


class DocumentFormat(enum.Enum):
    MARKDOWN = "MARKDOWN"
    PDF = "PDF"