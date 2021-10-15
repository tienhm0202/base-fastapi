from typing import Any

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette_prometheus import PrometheusMiddleware, metrics

from .. import get_logger

logger = get_logger(__name__)


def init_app(app: FastAPI, settings: Any):
    init_sentry(app, settings)
    init_prometheus(app, settings)


def init_sentry(app: FastAPI, settings: Any) -> None:
    if getattr(settings, "SENTRY_DSN",
               None) and settings.SERVER_ENV == "production":
        logger.info("Middleware enabled: SentryAsgiMiddleware")
        sentry_sdk.init(dsn=settings.SENTRY_DSN,
                        release=settings.SERVER_VERSION,
                        server_name=settings.SERVER_NAME,
                        environment=settings.SERVER_ENV,
                        in_app_include=settings.SENTRY_INCLUDE,
                        traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
                        integrations=[SqlalchemyIntegration()])
        app.add_middleware(SentryAsgiMiddleware)


def init_prometheus(app: FastAPI, settings: Any):
    if getattr(settings, "PROMETHEUS_ENABLE", None):
        logger.info("Middleware enabled: PrometheusMiddleware")
        app.add_middleware(PrometheusMiddleware)
        app.add_route(settings.PROMETHEUS_PATH, metrics)
