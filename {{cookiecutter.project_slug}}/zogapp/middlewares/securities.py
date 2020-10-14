from fastapi import FastAPI
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.rate_limiting.middleware import RateLimitingMiddleware, \
    InMemoryLimitProvider
from starlette.middleware.cors import CORSMiddleware

from zogapp import settings


def init_app(app: FastAPI) -> None:
    init_csrf(app)
    init_cors(app)
    init_rate_limiter(app)


def init_csrf(app: FastAPI) -> None:
    if settings.SECURITY_CSRF:
        app.add_middleware(CSRFMiddleware, allowed_hosts=[settings.SERVER_HOST])


def init_cors(app: FastAPI) -> None:
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def init_rate_limiter(app: FastAPI) -> None:
    if settings.RATE_LIMIT:
        provider = InMemoryLimitProvider(
            limit=settings.RATE_LIMIT,
            timespan=settings.RATE_LIMIT_TIME_SPAN,
            block_duration=settings.RATE_LIMIT_BLOCK_DURATION
        )
        app.add_middleware(
            RateLimitingMiddleware, provider=provider
        )
