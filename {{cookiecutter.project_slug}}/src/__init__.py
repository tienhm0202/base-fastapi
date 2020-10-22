from fastapi import FastAPI
from zogutils import middlewares


from . import modules
from .config import settings


def create_app() -> FastAPI:
    my_app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    middlewares.init_app(my_app, settings)
    modules.init_app(my_app)
    return my_app
