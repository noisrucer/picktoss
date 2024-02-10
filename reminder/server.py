from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from reminder.domain.category.model import Category
from reminder.domain.document.model import Document
from reminder.domain.question.model import Question, QuestionQuestionSet, QuestionSet
from reminder.core.database.session_manager import Base, sessionmanager
from reminder.core.exception.base import BaseCustomException
from reminder.domain.category.controller import router as category_router
from reminder.domain.document.controller import router as post_router
from reminder.domain.member.controller import router as member_router
from reminder.domain.question.controller import router as question_router
from fastapi.middleware.cors import CORSMiddleware


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
    app.include_router(member_router, prefix="/api/v1")
    app.include_router(category_router, prefix="/api/v1")
    app.include_router(question_router, prefix="/api/v1")


def init_middlewares(app: FastAPI) -> None:
    origins = ["http://localhost:5173"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    # @app.middleware("http")
    # async def cors_handlers(request: Request, call_next):
    #     response: Response = await call_next(request)
    #     response.headers['Access-Control-Allow-Credentials'] = 'true'
    #     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    #     response.headers['Access-Control-Allow-Methods'] = "CONNECT, DEBUG, DELETE, DONE, GET, HEAD, HTTP, HTTP/0.9, HTTP/1.0, HTTP/1.1, HTTP/2, OPTIONS, ORIGIN, ORIGINS, PATCH, POST, PUT, QUIC, REST, SESSION, SHOULD, SPDY, TRACE, TRACK"
    #     response.headers['Access-Control-Allow-Headers'] = 'Accept, Accept-CH, Accept-Charset, Accept-Datetime, Accept-Encoding, Accept-Ext, Accept-Features, Accept-Language, Accept-Params, Accept-Ranges, Access-Control-Allow-Credentials, Access-Control-Allow-Headers, Access-Control-Allow-Methods, Access-Control-Allow-Origin, Access-Control-Expose-Headers, Access-Control-Max-Age, Access-Control-Request-Headers, Access-Control-Request-Method, Age, Allow, Alternates, Authentication-Info, Authorization, C-Ext, C-Man, C-Opt, C-PEP, C-PEP-Info, CONNECT, Cache-Control, Compliance, Connection, Content-Base, Content-Disposition, Content-Encoding, Content-ID, Content-Language, Content-Length, Content-Location, Content-MD5, Content-Range, Content-Script-Type, Content-Security-Policy, Content-Style-Type, Content-Transfer-Encoding, Content-Type, Content-Version, Cookie, Cost, DAV, DELETE, DNT, DPR, Date, Default-Style, Delta-Base, Depth, Derived-From, Destination, Differential-ID, Digest, ETag, Expect, Expires, Ext, From, GET, GetProfile, HEAD, HTTP-date, Host, IM, If, If-Match, If-Modified-Since, If-None-Match, If-Range, If-Unmodified-Since, Keep-Alive, Label, Last-Event-ID, Last-Modified, Link, Location, Lock-Token, MIME-Version, Man, Max-Forwards, Media-Range, Message-ID, Meter, Negotiate, Non-Compliance, OPTION, OPTIONS, OWS, Opt, Optional, Ordering-Type, Origin, Overwrite, P3P, PEP, PICS-Label, POST, PUT, Pep-Info, Permanent, Position, Pragma, ProfileObject, Protocol, Protocol-Query, Protocol-Request, Proxy-Authenticate, Proxy-Authentication-Info, Proxy-Authorization, Proxy-Features, Proxy-Instruction, Public, RWS, Range, Referer, Refresh, Resolution-Hint, Resolver-Location, Retry-After, Safe, Sec-Websocket-Extensions, Sec-Websocket-Key, Sec-Websocket-Origin, Sec-Websocket-Protocol, Sec-Websocket-Version, Security-Scheme, Server, Set-Cookie, Set-Cookie2, SetProfile, SoapAction, Status, Status-URI, Strict-Transport-Security, SubOK, Subst, Surrogate-Capability, Surrogate-Control, TCN, TE, TRACE, Timeout, Title, Trailer, Transfer-Encoding, UA-Color, UA-Media, UA-Pixels, UA-Resolution, UA-Windowpixels, URI, Upgrade, User-Agent, Variant-Vary, Vary, Version, Via, Viewport-Width, WWW-Authenticate, Want-Digest, Warning, Width, X-Content-Duration, X-Content-Security-Policy, X-Content-Type-Options, X-CustomHeader, X-DNSPrefetch-Control, X-Forwarded-For, X-Forwarded-Port, X-Forwarded-Proto, X-Frame-Options, X-Modified, X-OTHER, X-PING, X-PINGOTHER, X-Powered-By, X-Requested-With'
    #     return response


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with sessionmanager._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

    app = FastAPI(title="peerloop server", description="peerloop server", version="0.1.0", lifespan=lifespan)

    @app.get("/health-check")
    async def health_check():
        return "I'm very healthy. Don't worry"
    
    init_exception_handlers(app)
    init_routers(app)
    init_middlewares(app)

    return app


app = create_app()
