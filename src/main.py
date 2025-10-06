import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient

from .core.config import settings
from .core.logs import setup_logging
from .frontend import create_frontend_app
from .routers.frontend import router as frontend_router
from .services.gotenberg import create_gotenberg_client
from .services.s3 import S3StorageService

setup_logging(
    level=logging.DEBUG if settings.debug else logging.INFO,
    log_file=Path("logs/app.log"),
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with (
        create_gotenberg_client(settings.gotenberg) as gotenberg_client,
        S3StorageService(settings.s3) as storage_service,
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
        app.state.gotenberg_client = gotenberg_client
        app.state.storage_service = storage_service
        yield


app = FastAPI(debug=settings.debug, lifespan=lifespan)

app.include_router(frontend_router, prefix="/frontend-api")

frontend_app = create_frontend_app()
app.mount("/", frontend_app)
