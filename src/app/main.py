import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import auth, customers, health, plans, subscribers
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "application_startup environment=%s",
        settings.environment,
    )

    yield

    logger.info("application_shutdown")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="MTN-style subscriber and service management API",
    debug=settings.debug,
    lifespan=lifespan,
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4()),
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request method=%s path=%s status=%s request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        request_id,
    )

    return response


@app.exception_handler(Exception)
async def unhandled_exception(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "unhandled_exception path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )


app.include_router(
    health.router,
    prefix="/api/v1",
)

app.include_router(
    auth.router,
    prefix="/api/v1",
)

app.include_router(
    customers.router,
    prefix="/api/v1",
)

app.include_router(
    subscribers.router,
    prefix="/api/v1",
)

app.include_router(
    plans.router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": app.version,
        "status": "running",
    }
