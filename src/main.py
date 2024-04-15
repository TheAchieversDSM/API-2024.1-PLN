from fastapi import FastAPI
from .config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from .routes import define_routes
from .config.dependency import nltk_dependencies_manager


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/docs",
        on_startup=[nltk_dependencies_manager],
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
define_routes(app)
