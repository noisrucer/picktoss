from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from reminder.core.database.session_manager import Base, sessionmanager
from reminder.core.exception.base import BaseCustomException
from reminder.domain.document.controller import router as post_router


def init_exception_handlers(app: FastAPI) -> None:
    """Initialize exception handlers."""

    @app.exception_handler(Exception)
    def handle_root_exception(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BaseCustomException)
    def handle_custom_exception(request: Request, exc: BaseCustomException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    def handle_fastapi_request_exception(request: Request, exc: RequestValidationError) -> JSONResponse:
        err = exc.errors()[0]
        inp = err["input"]
        loc = err["loc"]

        msg = f"Invalid {loc[-1]}: '{inp}' is invalid. {err['msg']}"
        return JSONResponse(
            status_code=400,
            content={"detail": msg},
        )


def init_routers(app: FastAPI) -> None:
    app.include_router(post_router, prefix="/api/v1")


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with sessionmanager._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

    app = FastAPI(title="peerloop server", description="peerloop server", version="0.1.0", lifespan=lifespan)

    init_exception_handlers(app)
    init_routers(app)

    @app.get("/")
    async def hello():
        return "go away"

    return app


app = create_app()
