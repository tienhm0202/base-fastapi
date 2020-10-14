from fastapi import FastAPI

from . import securities, monitoring


def init_app(app: FastAPI):
    monitoring.init_app(app)
    securities.init_app(app)
