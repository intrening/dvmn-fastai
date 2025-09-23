from fastapi import FastAPI

from .sites.routes import router as sites_router
from .users.routes import router as users_router


def create_frontend_api_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users_router)
    app.include_router(sites_router)
    return app


__all__ = ["create_frontend_api_app"]
