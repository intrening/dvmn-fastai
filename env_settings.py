from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# class DatabaseSettings(BaseSettings):
#     host: str = "localhost"
#     port: int = 5432


class UnsplashSettings(BaseSettings):
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


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_default=True,
        env_nested_delimiter="__",
        use_attribute_docstrings=True,
    )

    unsplash: UnsplashSettings = Field(
        ...,
        description="Unsplash API settings",
    )

    debug: bool = False
