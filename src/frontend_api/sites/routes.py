import asyncio
from collections.abc import AsyncGenerator
from datetime import datetime

import aiofiles
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse

from .schemas import (
    CreateSiteRequest,
    GeneratedSiteResponse,
    SiteGenerateRequest,
    SiteResponse,
)

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
        title="Сайт о стегозаврах",
        prompt=request.prompt,
        screenshot_url=None,
        html_code_url=None,
        html_code_download_url=None,
        created_at=datetime(2025, 6, 15, 18, 29, 56),
        updated_at=datetime(2025, 6, 15, 18, 29, 56),
    )


async def site_generate_logic(site_id: int, prompt: str) -> AsyncGenerator[str, None]:
    file_path = "index.html"
    try:
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            async for line in f:
                yield line
                await asyncio.sleep(0.05)
    except FileNotFoundError:
        yield "<html><body><h1>Site not found</h1></body></html>"


@router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать сайт",
    description="Сгенерировать сайт по ID.",
)
async def generate_site(site_id: int, request: SiteGenerateRequest) -> StreamingResponse:
    return StreamingResponse(
        content=site_generate_logic(site_id, request.prompt),
        media_type="text/html",
    )


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
                title="Сайт о стегозаврах",
                prompt="Сайт о стегозаврах",
                screenshot_url=None,
                html_code_url="http://127.0.0.1:8000/frontend-api/media/index.html",
                html_code_download_url="http://127.0.0.1:8000/frontend-api/media/index.html?response-content-disposition=attachment",
                created_at=datetime(2025, 6, 15, 18, 29, 56),
                updated_at=datetime(2025, 6, 15, 18, 29, 56),
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
        title="Сайт о стегозаврах",
        prompt="Сайт о стегозаврах",
        screenshot_url=None,
        html_code_url="http://127.0.0.1:8000/frontend-api/media/index.html",
        html_code_download_url="http://127.0.0.1:8000/frontend-api/media/index.html?response-content-disposition=attachment",
        created_at=datetime(2025, 6, 15, 18, 29, 56),
        updated_at=datetime(2025, 6, 15, 18, 29, 56),
    )


@router.get(
    "/media/index.html",
    summary="Получить index.html",
    description="Выдать файл index.html из корневой папки",
)
async def get_index_html() -> FileResponse:
    return FileResponse("index.html", media_type="text/html")


__all__ = ["router"]
