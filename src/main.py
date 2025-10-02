import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from httpx import Limits

from .core.config import AppSettings
from .core.logs import setup_logging
from .frontend import create_frontend_app
from .frontend_api.app import create_frontend_api_app
from .services.s3 import S3Service

settings = AppSettings()

setup_logging(
    level=logging.DEBUG if settings.debug else logging.INFO,
    log_file=Path("logs/app.log"),
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    gotenberg_client = httpx.AsyncClient(
        base_url=settings.gotenberg.url,
        timeout=settings.gotenberg.timeout,
        limits=Limits(
            max_connections=settings.gotenberg.max_connections,
        ),
    )
    async with (
        gotenberg_client as entered_gotenberg_client,
        S3Service(settings.s3) as s3_service,
        AsyncUnsplashClient.setup(
            unsplash_client_id=settings.unsplash.access_key.get_secret_value(),
            timeout=settings.unsplash.timeout,
        ),
        AsyncDeepseekClient.setup(
            settings.deepseek.api_key.get_secret_value(),
            settings.deepseek.base_url,
            settings.deepseek.model,
        ),
    ):
        app.state.gotenberg_client = entered_gotenberg_client
        app.state.s3_service = s3_service
        yield


app = FastAPI(debug=settings.debug, lifespan=lifespan)

frontend_api_app = create_frontend_api_app()
app.mount("/frontend-api", frontend_api_app)

frontend_app = create_frontend_app()
app.mount("/", frontend_app)
