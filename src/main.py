from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient

from .core.config import AppSettings
from .frontend import create_frontend_app
from .frontend_api.app import api_router as frontend_api_router

settings = AppSettings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with (
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
        yield


app = FastAPI(debug=settings.debug, lifespan=lifespan)
app.include_router(frontend_api_router)

frontend_app = create_frontend_app()
app.mount("/", frontend_app)
