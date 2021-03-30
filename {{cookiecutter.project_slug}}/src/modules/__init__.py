from fastapi import APIRouter, FastAPI

from src.config import settings

# Add modules in here
load_modules = []


def init_app(app: FastAPI):
    router = APIRouter()
    for module in load_modules:
        router.include_router(
            module.controllers.router,
            prefix=module.API_PREFIX,
            tags=module.API_TAGS
        )  # noqa

    app.include_router(router, prefix=settings.API_V1_STR)
