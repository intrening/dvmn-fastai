import asyncio
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Annotated

import aiofiles
from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt
from pydantic.alias_generators import to_camel

from .apps.frontend import create_frontend_app

api_router = APIRouter(prefix="/frontend-api")

UserName = Annotated[
    str,
    Field(
        max_length=254,
        examples=["ivan", "alex123"],
    ),
]


class UserDetailsResponse(BaseModel):
    """Информация о текущем пользователе"""

    email: EmailStr = Field(description="Email пользователя")
    is_active: bool = Field(description="Активен ли пользователь")
    profile_id: PositiveInt = Field(description="ID профиля пользователя")
    registered_at: datetime = Field(description="Дата регистрации пользователя")
    updated_at: datetime = Field(description="Дата обновления профиля пользователя")
    username: UserName = Field(description="Имя пользователя")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "example@example.com",
                    "is_active": True,
                    "profile_id": "1",
                    "registered_at": "2025-06-15T18:29:56+00:00",
                    "updated_at": "2025-06-15T18:29:56+00:00",
                    "username": "user123",
                },
            ],
        },
    )


@api_router.get(
    "/users/me",
    response_model=UserDetailsResponse,
    summary="Получить информацию о текущем пользователе",
    description="Возвращает данные профиля текущего авторизованного пользователя.",
)
async def me() -> UserDetailsResponse:
    return UserDetailsResponse(
        email="example@example.com",
        is_active=True,
        profile_id=1,
        registered_at=datetime(2025, 6, 15, 18, 29, 56),
        updated_at=datetime(2025, 6, 15, 18, 29, 56),
        username="user123",
    )


class CreateSiteRequest(BaseModel):
    """Запрос на создание сайта"""

    title: str | None = Field(default=None, description="Название сайта")
    prompt: str = Field(description="Prompt для создания сайта")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "prompt": "Сайт любителей играть в домино",
                    "title": "Фан клуб игры в домино",
                },
            ],
        },
    )


class SiteResponse(BaseModel):
    """Информация о сайте"""

    id: PositiveInt = Field(description="ID сайта")
    title: str = Field(description="Название сайта")
    html_code_url: str | None = Field(default=None, description="URL HTML кода сайта")
    html_code_download_url: str | None = Field(default=None, description="URL скачивания HTML кода сайта")
    screenshot_url: str | None = Field(default=None, description="URL скриншота сайта")
    prompt: str = Field(description="Prompt для создания сайта")
    created_at: datetime = Field(description="Дата создания сайта")
    updated_at: datetime = Field(description="Дата обновления сайта")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "created_at": datetime(2025, 6, 15, 18, 29, 56).isoformat(),
                    "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
                    "html_code_url": "http://example.com/media/index.html",
                    "id": 1,
                    "prompt": "Сайт любителей играть в домино",
                    "screenshot_url": "http://example.com/media/index.png",
                    "title": "Фан клуб Домино",
                    "updated_at": datetime(2025, 6, 15, 18, 29, 56).isoformat(),
                },
            ],
        },
    )


class GeneratedSiteResponse(SiteResponse):
    """Информация о сгенерированном сайте"""

    pass


@api_router.post(
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


class SiteGenerateRequest(BaseModel):
    """Запрос на генерацию сайта"""

    prompt: str = Field(description="Prompt для создания сайта")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "prompt": "Сайт о стегозаврах",
                },
            ],
        },
    )


async def site_generate_logic(site_id: int, prompt: str) -> AsyncGenerator[str, None]:
    file_path = "index.html"
    try:
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            async for line in f:
                yield line
                await asyncio.sleep(0.00001)
    except FileNotFoundError:
        yield "<html><body><h1>Site not found</h1></body></html>"


@api_router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать сайт",
    description="Сгенерировать сайт по ID.",
)
async def generate_site(site_id: int, request: SiteGenerateRequest) -> StreamingResponse:
    return StreamingResponse(
        content=site_generate_logic(site_id, request.prompt),
        media_type="text/html",
    )


@api_router.get(
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


@api_router.get(
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


@api_router.get(
    "/media/index.html",
    summary="Получить index.html",
    description="Выдать файл index.html из корневой папки",
)
async def get_index_html() -> FileResponse:
    return FileResponse("index.html", media_type="text/html")


app = FastAPI()
app.include_router(api_router)


frontend_app = create_frontend_app()
app.mount("/", frontend_app)
