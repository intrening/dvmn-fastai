import logging
from typing import Any, Literal, Optional

import httpx
from gotenberg_api import ScreenshotHTMLRequest
from httpx import Limits

from ..core.config import GotenbergSettings

logger = logging.getLogger(__name__)


class GotenbergService:
    def __init__(self, settings: GotenbergSettings) -> None:
        self.settings = settings
        self._client: Optional[httpx.AsyncClient] = None

    async def connect(self) -> None:
        if self._client is not None:
            logger.warning("Gotenberg client already connected")
            return

        self._client = httpx.AsyncClient(
            base_url=self.settings.url,
            timeout=self.settings.timeout,
            limits=Limits(
                max_connections=self.settings.max_connections,
            ),
        )

    async def disconnect(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "GotenbergService":
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.disconnect()

    async def screenshot_html(
        self,
        html_code: str,
        width: Optional[int] = None,
        screenshot_format: Optional[Literal["png", "jpeg", "webp"]] = None,
        wait_delay: Optional[int] = None,
    ) -> bytes:
        if self._client is None:
            raise RuntimeError(
                "Gotenberg client is not initialized. Use async context manager.",
            )

        screenshot_bytes = await ScreenshotHTMLRequest(
            index_html=html_code,
            width=width or self.settings.screenshot_width,
            format=screenshot_format or self.settings.screenshot_format.value,
            wait_delay=wait_delay or self.settings.wait_delay,
        ).asend(self._client)

        return screenshot_bytes
