from fastapi import FastAPI
from .api import router as doc_route


def define_routes(app: FastAPI):
    app.include_router(doc_route)
