import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics

from zogapp import settings


def init_app(app: FastAPI):
    init_sentry(app)
    init_prometheus(app)


def init_sentry(app: FastAPI) -> None:
    if settings.SENTRY_DSN:
        sentry_sdk.init(dsn=settings.SENTRY_DSN,
                        release=settings.SERVER_VERSION,
                        server_name=settings.SERVER_NAME,
                        environment=settings.SERVER_ENV,
                        in_app_include=settings.SENTRY_INCLUDE)
        app.add_middleware(SentryAsgiMiddleware)


def init_prometheus(app: FastAPI):
    if settings.PROMETHEUS_ENABLE:
        app.add_middleware(PrometheusMiddleware)
        app.add_route(settings.PROMETHEUS_PATH, metrics)
