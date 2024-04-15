from fastapi import FastAPI
from .api import router as doc_route
from .pln import router as pln_route


def define_routes(app: FastAPI):
    app.include_router(doc_route)
    app.include_router(pln_route)
