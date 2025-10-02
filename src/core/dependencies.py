"""FastAPI dependency injection functions."""

import logging

from fastapi import Request

from ..core.config import AppSettings
from ..services.gotenberg import GotenbergService
from ..services.s3 import S3Service

logger = logging.getLogger(__name__)

settings = AppSettings()


async def get_s3_service(request: Request) -> S3Service:
    s3: S3Service | None = getattr(request.app.state, "s3_service", None)

    if s3 is None:
        logger.warning("S3 service not found in app state, creating new instance")
        s3 = S3Service(settings.s3)
        await s3.connect()
        request.app.state.s3_service = s3

    return s3


async def get_gotenberg_service(request: Request) -> GotenbergService:
    gotenberg: GotenbergService | None = getattr(
        request.app.state,
        "gotenberg_service",
        None,
    )

    if gotenberg is None:
        logger.warning(
            "Gotenberg service not found in app state, creating new instance",
        )
        gotenberg = GotenbergService(settings.gotenberg)
        await gotenberg.connect()
        request.app.state.gotenberg_service = gotenberg

    return gotenberg
