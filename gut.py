import asyncio

import httpx
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest

from src.core.config import AppSettings

settings_var = AppSettings()
GOTENBERG_URL = "https://demo.gotenberg.dev"

with open("index.html", "r", encoding="utf-8") as file:
    raw_html = file.read()


async def main() -> None:
    try:
        async with httpx.AsyncClient(
            base_url=GOTENBERG_URL,
            timeout=15,
        ) as client:
            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=raw_html,
                width=1000,
                format="png",
                wait_delay=5,
            ).asend(client)
    except GotenbergServerError as e:
        print(e)
        screenshot_bytes = None

    with open("screenshot.png", "wb") as file:
        file.write(screenshot_bytes)


def main_sync() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()
