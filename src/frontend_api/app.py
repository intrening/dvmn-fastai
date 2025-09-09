from fastapi import APIRouter

from .sites.routes import router as sites_router
from .users.routes import router as users_router

api_router = APIRouter(prefix="/frontend-api")
api_router.include_router(users_router)
api_router.include_router(sites_router)

__all__ = ["api_router"]
