import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aioboto3.session import AioConfig, Session
from fastapi import FastAPI
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient

from .core.config import AppSettings
from .frontend import create_frontend_app
from .frontend_api.app import api_router as frontend_api_router

settings = AppSettings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    s3_config = AioConfig(
        max_pool_connections=settings.aws.max_pool_connections,
        connect_timeout=settings.aws.connect_timeout,
        read_timeout=settings.aws.read_timeout,
    )
    s3_session = Session(
        aws_access_key_id=settings.aws.access_key.get_secret_value(),
        aws_secret_access_key=settings.aws.secret_key.get_secret_value(),
    )
    async with (
        s3_session.client(
            "s3",
            endpoint_url=settings.aws.endpoint_url,
            config=s3_config,
        ) as s3_client,
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
        app.state.s3_client = s3_client
        yield


app = FastAPI(debug=settings.debug, lifespan=lifespan)
app.include_router(frontend_api_router)

frontend_app = create_frontend_app()
app.mount("/", frontend_app)
