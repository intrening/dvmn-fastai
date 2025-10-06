from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal, Optional

import httpx
from gotenberg_api import ScreenshotHTMLRequest
from httpx import Limits

from ..core.config import GotenbergSettings


@asynccontextmanager
async def create_gotenberg_client(settings: GotenbergSettings) -> AsyncIterator[httpx.AsyncClient]:
    client = httpx.AsyncClient(
        base_url=settings.url,
        timeout=settings.timeout,
        limits=Limits(max_connections=settings.max_connections),
    )
    try:
        yield client
    finally:
        await client.aclose()


async def screenshot_html(
    client: httpx.AsyncClient,
    settings: GotenbergSettings,
    html_code: str,
    width: Optional[int] = None,
    screenshot_format: Optional[Literal["png", "jpeg", "webp"]] = None,
    wait_delay: Optional[int] = None,
) -> bytes:
    return await ScreenshotHTMLRequest(
        index_html=html_code,
        width=width or settings.screenshot_width,
        format=screenshot_format or settings.screenshot_format.value,
        wait_delay=wait_delay or settings.wait_delay,
    ).asend(client)
