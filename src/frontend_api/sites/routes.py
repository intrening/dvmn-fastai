from collections.abc import AsyncGenerator
from datetime import datetime

import anyio
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, StreamingResponse
from furl import furl
from html_page_generator import AsyncPageGenerator

from .schemas import (
    CreateSiteRequest,
    GeneratedSiteResponse,
    SiteGenerateRequest,
    SiteResponse,
)
from ...core.config import AppSettings

GENERATED_HTML_FILE = "index.html"
MOCK_TITLE = "Тестовый сайт"
MOCK_PROMPT = "Тестовый промпт для сайта"
MOCK_SCREENSHOT_URL = None
MOCK_HTML_CODE_URL = "http://127.0.0.1:8000/frontend-api/media/index.html"
MOCK_HTML_CODE_DOWNLOAD_URL = (
    "http://127.0.0.1:8000/frontend-api/media/index.html?response-content-disposition=attachment"
)
MOCK_CREATED_AT = datetime(2025, 6, 15, 18, 29, 56)
MOCK_UPDATED_AT = datetime(2025, 6, 15, 18, 29, 56)


def generated_html_file_url() -> str:
    html_file_url = furl(settings.aws.endpoint_url)
    html_file_url.path.add(settings.aws.bucket_name)
    html_file_url.path.add(GENERATED_HTML_FILE)
    html_file_url.args["response-content-disposition"] = "inline"
    return html_file_url.url


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
        id=1,
        title=MOCK_TITLE,
        prompt=request.prompt,
        screenshot_url=MOCK_SCREENSHOT_URL,
        html_code_url=MOCK_HTML_CODE_URL,
        html_code_download_url=MOCK_HTML_CODE_DOWNLOAD_URL,
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


@router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать сайт",
    description="Сгенерировать сайт по ID. Стримит HTML и параллельно пишет в index.html",
)
async def generate_site(site_id: int, request: SiteGenerateRequest) -> StreamingResponse:
    html_chunks = AsyncPageGenerator(
        debug_mode=settings.debug,
    ).generate_html(request.prompt)

    async def stream_and_write() -> AsyncGenerator[str, None]:
        async with await anyio.open_file(GENERATED_HTML_FILE, mode="w", encoding="utf-8") as html_file:
            try:
                async for html_chunk in html_chunks:
                    await html_file.write(html_chunk)
                    yield html_chunk
            except anyio.get_cancelled_exc_class():
                with anyio.CancelScope(shield=True):
                    async for html_chunk in html_chunks:
                        await html_file.write(html_chunk)
                raise

    return StreamingResponse(content=stream_and_write(), media_type="text/html")


@router.get(
    "/sites/my",
    summary="Получить список сайтов текущего пользователя",
    description="Выдать список сайтов текущего пользователя",
)
async def get_sites_my() -> dict[str, list[SiteResponse]]:
    return {
        "sites": [
            SiteResponse(
                id=1,
                title=MOCK_TITLE,
                prompt=MOCK_PROMPT,
                screenshot_url=None,
                html_code_url=MOCK_HTML_CODE_URL,
                html_code_download_url=MOCK_HTML_CODE_DOWNLOAD_URL,
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
        id=site_id,
        title=MOCK_TITLE,
        prompt=MOCK_PROMPT,
        screenshot_url=MOCK_SCREENSHOT_URL,
        html_code_url=MOCK_HTML_CODE_URL,
        html_code_download_url=MOCK_HTML_CODE_DOWNLOAD_URL,
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


@router.get(
    "/media/index.html",
    summary="Получить index.html",
    description="Вернуть ссылку на сайт (редирект на хранилище)",
)
async def get_index_html() -> RedirectResponse:
    return RedirectResponse(url=generated_html_file_url(), status_code=307)


__all__ = ["router"]
