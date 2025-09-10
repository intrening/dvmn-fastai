from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    debug: bool = False
