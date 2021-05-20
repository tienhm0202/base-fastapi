import pydantic
from fastapi import FastAPI

from . import securities, monitoring, exceptions, request_id, whitelist


def init_app(app: FastAPI, settings: pydantic.BaseSettings):
    whitelist.init_app(app, settings)
    monitoring.init_app(app, settings)
    securities.init_app(app, settings)
    exceptions.init_app(app)
    request_id.init_app(app)
