import logging
from collections.abc import AsyncGenerator
from datetime import datetime

import anyio
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from furl import furl
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator

from src.core.config import AppSettings
from src.core.dependencies import get_s3_service

from .schemas import (
    CreateSiteRequest,
    GeneratedSiteResponse,
    SiteGenerateRequest,
    SiteResponse,
)

logger = logging.getLogger(__name__)

MOCK_SITE_ID = 1
MOCK_TITLE = "Тестовый сайт"
MOCK_PROMPT = "Тестовый промпт для сайта"
MOCK_SITE_HTML_FILE_NAME = "mocked_site.html"
MOCK_SITE_SCREENSHOT_FILE_NAME = "mocked_site.png"
MOCK_CREATED_AT = datetime(2025, 6, 15, 18, 29, 56)
MOCK_UPDATED_AT = datetime(2025, 6, 15, 18, 29, 56)


def get_mock_site_html_file_url(is_download: bool = False) -> str:
    html_file_url = furl(settings.s3.endpoint_url)
    html_file_url.path.add(settings.s3.bucket_name)
    html_file_url.path.add(MOCK_SITE_HTML_FILE_NAME)
    html_file_url.args["response-content-disposition"] = "inline" if not is_download else "attachment"
    return html_file_url.url


def get_mock_screenshot_url() -> str:
    screenshot_file_url = furl(settings.s3.endpoint_url)
    screenshot_file_url.path.add(settings.s3.bucket_name)
    screenshot_file_url.path.add(MOCK_SITE_SCREENSHOT_FILE_NAME)
    return screenshot_file_url.url


settings = AppSettings()
router = APIRouter(tags=["Sites"])


@router.post(
    "/sites/create",
    response_model=GeneratedSiteResponse,
    summary="Создать сайт",
    description="Создает сайт для текущего пользователя.",
)
async def create_site(request: CreateSiteRequest) -> GeneratedSiteResponse:
    return GeneratedSiteResponse(
        id=MOCK_SITE_ID,
        title=MOCK_TITLE,
        prompt=request.prompt,
        screenshot_url=get_mock_screenshot_url(),
        html_code_url=get_mock_site_html_file_url(),
        html_code_download_url=get_mock_site_html_file_url(is_download=True),
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


@router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать сайт",
    description="Сгенерировать сайт по ID. Стримит HTML и параллельно пишет в index.html",
)
async def generate_site(site_id: int, request: SiteGenerateRequest, req: Request) -> StreamingResponse:
    site_generator = AsyncPageGenerator(
        debug_mode=settings.debug,
    )

    async def stream_and_upload() -> AsyncGenerator[str, None]:
        with anyio.CancelScope(shield=True):
            async for html_chunk in site_generator(request.prompt):
                yield html_chunk

            html_code = site_generator.html_page.html_code
            s3_service = await get_s3_service(req)
            await s3_service.upload_file(
                data=html_code.encode("utf-8"),
                object_name=MOCK_SITE_HTML_FILE_NAME,
                content_type="text/html",
                content_disposition="inline",
            )

            try:
                client = req.app.state.gotenberg_client
                screenshot_bytes = await ScreenshotHTMLRequest(
                    index_html=html_code,
                    width=settings.gotenberg.screenshot_width,
                    format=settings.gotenberg.screenshot_format,
                    wait_delay=settings.gotenberg.wait_delay,
                ).asend(client)
                await s3_service.upload_file(
                    data=screenshot_bytes,
                    object_name=MOCK_SITE_SCREENSHOT_FILE_NAME,
                    content_type="image/png",
                )
            except GotenbergServerError as e:
                logger.error(e)

    return StreamingResponse(content=stream_and_upload(), media_type="text/html")


@router.get(
    "/sites/my",
    summary="Получить список сайтов текущего пользователя",
    description="Выдать список сайтов текущего пользователя",
)
async def get_sites_my() -> dict[str, list[SiteResponse]]:
    return {
        "sites": [
            SiteResponse(
                id=MOCK_SITE_ID,
                title=MOCK_TITLE,
                prompt=MOCK_PROMPT,
                screenshot_url=get_mock_screenshot_url(),
                html_code_url=get_mock_site_html_file_url(),
                html_code_download_url=get_mock_site_html_file_url(is_download=True),
                created_at=MOCK_CREATED_AT,
                updated_at=MOCK_UPDATED_AT,
            ),
        ],
    }


@router.get(
    "/sites/{site_id}",
    summary="Получить сайт",
    description="Получить сайт по ID.",
)
async def get_site(site_id: int) -> SiteResponse:
    return SiteResponse(
        id=MOCK_SITE_ID,
        title=MOCK_TITLE,
        prompt=MOCK_PROMPT,
        screenshot_url=get_mock_screenshot_url(),
        html_code_url=get_mock_site_html_file_url(),
        html_code_download_url=get_mock_site_html_file_url(is_download=True),
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


@router.get(
    "/media/mocked_site.html",
    summary="Получить HTML код сайта",
    description="Вернуть ссылку на сайт (редирект на хранилище)",
)
async def get_index_html() -> RedirectResponse:
    return RedirectResponse(url=get_mock_site_html_file_url(), status_code=307)


__all__ = ["router"]
