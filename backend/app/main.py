from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)
    register_exception_handlers(application)
    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
