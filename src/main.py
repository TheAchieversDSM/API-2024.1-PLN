from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.database import init_db, finish_db
from src.config.settings import settings
from src.routes import define_routes


def get_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME, docs_url="/docs", on_startup=[init_db], on_shutdown=[finish_db])

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
