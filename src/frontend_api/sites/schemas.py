from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from pydantic.alias_generators import to_camel


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


__all__ = [
    "CreateSiteRequest",
    "SiteResponse",
    "GeneratedSiteResponse",
    "SiteGenerateRequest",
]
