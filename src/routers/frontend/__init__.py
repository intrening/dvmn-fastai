"""Frontend-facing API routers."""

from fastapi import APIRouter

from .sites.routes import router as sites_router
from .users.routes import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(sites_router)


__all__ = ["router"]
