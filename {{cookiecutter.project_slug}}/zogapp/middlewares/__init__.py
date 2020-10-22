from fastapi import FastAPI

from . import securities, monitoring, logger


def init_app(app: FastAPI):
    logger.init_app()
    monitoring.init_app(app)
    securities.init_app(app)
