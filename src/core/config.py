from enum import Enum
from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ValidScreenshotFormats(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


class GotenbergSettings(BaseSettings):
    """Gotenberg settings"""

    screenshot_width: int = Field(
        default=600,
        description="Gotenberg screenshot width",
        ge=1,
    )
    screenshot_format: ValidScreenshotFormats = Field(
        default=ValidScreenshotFormats.PNG,
        description="Gotenberg screenshot format",
    )
    url: str = Field(
        ...,
        description="Gotenberg URL",
    )
    max_connections: int = Field(
        default=5,
        description="Gotenberg max connections",
        ge=1,
    )
    timeout: int = Field(
        default=10,
        description="Gotenberg timeout",
        ge=1,
    )
    wait_delay: int = Field(
        default=8,
        description="Gotenberg screenshot wait delay (должен быть строго меньше timeout)",
        ge=1,
    )

    def model_post_init(self, __context: Any) -> None:
        if self.wait_delay >= self.timeout:
            raise ValueError("wait_delay должен быть строго меньше timeout")


class AWSSettings(BaseSettings):
    """AWS settings"""

    access_key: SecretStr = Field(
        ...,
        description="AWS access key",
    )
    secret_key: SecretStr = Field(
        ...,
        description="AWS secret key",
    )
    endpoint_url: str = Field(
        ...,
        description="AWS endpoint URL",
    )
    bucket_name: str = Field(
        ...,
        description="AWS bucket name",
    )
    read_timeout: int = Field(
        default=20,
        description="AWS read timeout",
        ge=1,
    )
    connect_timeout: int = Field(
        default=10,
        description="AWS connect timeout",
        ge=1,
    )
    max_pool_connections: int = Field(
        default=10,
        description="AWS max pool connections",
        ge=1,
    )


class DeepSeekSettings(BaseSettings):
    """DeepSeek API settings"""

    api_key: SecretStr = Field(
        ...,
        description="DeepSeek API key",
    )
    max_connections: int | None = Field(
        default=None,
        description="DeepSeek API max connections",
        ge=1,
    )
    timeout: int = Field(
        default=20,
        description="DeepSeek API timeout",
        ge=1,
    )
    base_url: str = Field(
        default="https://api.deepseek.com/v1",
        description="DeepSeek API base URL",
    )
    model: str = Field(
        default="deepseek-chat",
        description="DeepSeek model name",
    )


class UnsplashSettings(BaseSettings):
    """Unsplash API settings"""

    app_id: str = Field(
        ...,
        description="Unsplash API app ID",
    )
    access_key: SecretStr = Field(
        ...,
        description="Unsplash API access key",
    )
    secret_key: SecretStr = Field(
        ...,
        description="Unsplash API secret key",
    )
    max_connections: int | None = Field(
        default=5,
        description="Unsplash API max connections",
        ge=1,
    )
    timeout: int = Field(
        default=20,
        description="Unsplash API timeout",
        ge=1,
    )


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_default=True,
        env_nested_delimiter="__",
        use_attribute_docstrings=True,
        extra="forbid",
    )

    unsplash: UnsplashSettings
    deepseek: DeepSeekSettings
    aws: AWSSettings
    gotenberg: GotenbergSettings
    debug: bool = False
