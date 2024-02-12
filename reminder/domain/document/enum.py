import enum


class DocumentStatus(enum.Enum):
    UNPROCESSED = "UNPROCESSED"
    PROCESSED = "PROCESSED"
    COMPLETELY_FAILED = "COMPLETELY_FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"


class DocumentFormat(enum.Enum):
    MARKDOWN = "MARKDOWN"
