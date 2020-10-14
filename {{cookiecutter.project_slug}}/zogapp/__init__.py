from fastapi import FastAPI

from .config import settings
from . import middlewares


def create_app() -> FastAPI:
    my_app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    middlewares.init_app(my_app)
    return my_app
