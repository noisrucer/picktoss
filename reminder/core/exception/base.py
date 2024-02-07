from abc import ABC


class BaseCustomException(ABC, Exception):
    status_code: int
    detail: str

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}"
