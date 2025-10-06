import logging
from collections.abc import AsyncGenerator

import anyio
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from gotenberg_api import GotenbergServerError
from html_page_generator import AsyncPageGenerator

from src.core.config import settings
from src.core.dependencies import get_gotenberg_service, get_s3_service
from src.frontend_api.mocks import (
    MOCK_SITE_HTML_FILE_NAME,
    MOCK_SITE_SCREENSHOT_FILE_NAME,
    get_mock_generated_site_response,
    get_mock_site_html_file_url,
    get_mock_site_response,
)

from .schemas import (
    CreateSiteRequest,
    GeneratedSiteResponse,
    SiteGenerateRequest,
    SiteResponse,
)

logger = logging.getLogger(__name__)


router = APIRouter(tags=["Sites"])


@router.post(
    "/sites/create",
    response_model=GeneratedSiteResponse,
    summary="Создать сайт",
    description="Создает сайт для текущего пользователя.",
)
async def create_site(request: CreateSiteRequest) -> GeneratedSiteResponse:
    return get_mock_generated_site_response(request)


async def _stream_and_upload(
    site_generator: AsyncPageGenerator,
    request: SiteGenerateRequest,
    req: Request,
) -> AsyncGenerator:
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
            gotenberg_service = await get_gotenberg_service(req)
            screenshot_bytes = await gotenberg_service.screenshot_html(
                html_code=html_code,
            )
        except GotenbergServerError as e:
            logger.error(e)
        await s3_service.upload_file(
            data=screenshot_bytes,
            object_name=MOCK_SITE_SCREENSHOT_FILE_NAME,
            content_type="image/png",
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
    return StreamingResponse(content=_stream_and_upload(site_generator, request, req), media_type="text/html")


@router.get(
    "/sites/my",
    summary="Получить список сайтов текущего пользователя",
    description="Выдать список сайтов текущего пользователя",
)
async def get_sites_my() -> dict[str, list[SiteResponse]]:
    return {
        "sites": [
            get_mock_site_response(),
        ],
    }


@router.get(
    "/sites/{site_id}",
    summary="Получить сайт",
    description="Получить сайт по ID.",
)
async def get_site(site_id: int) -> SiteResponse:
    return get_mock_site_response()


@router.get(
    "/media/mocked_site.html",
    summary="Получить HTML код сайта",
    description="Вернуть ссылку на сайт (редирект на хранилище)",
)
async def get_index_html() -> RedirectResponse:
    return RedirectResponse(url=get_mock_site_html_file_url(), status_code=307)


__all__ = ["router"]
