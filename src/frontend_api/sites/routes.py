from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, Request
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

GENERATED_SCREENSHOT_FILE = "index.png"
MOCK_TITLE = "Тестовый сайт"
MOCK_PROMPT = "Тестовый промпт для сайта"
MOCK_SCREENSHOT_URL = None
MOCK_CREATED_AT = datetime(2025, 6, 15, 18, 29, 56)
MOCK_UPDATED_AT = datetime(2025, 6, 15, 18, 29, 56)


def get_site_file_name(site_id: int) -> str:
    return f"{site_id}.html"


def get_site_html_file_url(site_id: int, is_download: bool = False) -> str:
    html_file_url = furl(settings.aws.endpoint_url)
    html_file_url.path.add(settings.aws.bucket_name)
    html_file_url.path.add(get_site_file_name(site_id))
    html_file_url.args["response-content-disposition"] = "inline" if not is_download else "attachment"
    return html_file_url.url


def get_mock_screenshot_url() -> str:
    screenshot_file_url = furl(settings.aws.endpoint_url)
    screenshot_file_url.path.add(settings.aws.bucket_name)
    screenshot_file_url.path.add(GENERATED_SCREENSHOT_FILE)
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
    site_id = 1
    return GeneratedSiteResponse(
        id=site_id,
        title=MOCK_TITLE,
        prompt=request.prompt,
        screenshot_url=get_mock_screenshot_url(),
        html_code_url=get_site_html_file_url(site_id),
        html_code_download_url=get_site_html_file_url(site_id, is_download=True),
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


@router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать сайт",
    description="Сгенерировать сайт по ID. Стримит HTML и параллельно пишет в index.html",
)
async def generate_site(site_id: int, request: SiteGenerateRequest, req: Request) -> StreamingResponse:
    html_chunks = AsyncPageGenerator(
        debug_mode=settings.debug,
    ).generate_html(request.prompt)

    async def stream_and_upload() -> AsyncGenerator[str, None]:
        s3_client = req.app.state.s3_client
        buffer = bytearray()
        try:
            async for html_chunk in html_chunks:
                if isinstance(html_chunk, str):
                    buffer.extend(html_chunk.encode("utf-8"))
                else:
                    buffer.extend(html_chunk)
                yield html_chunk
        finally:
            await s3_client.put_object(
                Bucket=settings.aws.bucket_name,
                Key=get_site_file_name(site_id),
                Body=bytes(buffer),
                ContentType="text/html",
                ContentDisposition="inline",
            )

    return StreamingResponse(content=stream_and_upload(), media_type="text/html")


@router.get(
    "/sites/my",
    summary="Получить список сайтов текущего пользователя",
    description="Выдать список сайтов текущего пользователя",
)
async def get_sites_my() -> dict[str, list[SiteResponse]]:
    site_id = 1
    return {
        "sites": [
            SiteResponse(
                id=site_id,
                title=MOCK_TITLE,
                prompt=MOCK_PROMPT,
                screenshot_url=get_mock_screenshot_url(),
                html_code_url=get_site_html_file_url(site_id),
                html_code_download_url=get_site_html_file_url(site_id, is_download=True),
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
        screenshot_url=get_mock_screenshot_url(),
        html_code_url=get_site_html_file_url(site_id),
        html_code_download_url=get_site_html_file_url(site_id, is_download=True),
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


@router.get(
    "/media/{site_id}.html",
    summary="Получить HTML код сайта",
    description="Вернуть ссылку на сайт (редирект на хранилище)",
)
async def get_index_html(site_id: int) -> RedirectResponse:
    return RedirectResponse(url=get_site_html_file_url(site_id), status_code=307)


__all__ = ["router"]
