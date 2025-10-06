from abc import ABC, abstractmethod
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, BinaryIO

import aiofiles
import furl
from aioboto3.session import AioConfig, Session

from ..core.config import S3Settings


class StorageService(ABC):
    """Абстрактный класс для сервиса хранилища файлов."""

    @abstractmethod
    async def __aenter__(self) -> "StorageService":
        """Вход в контекстный менеджер."""

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Выход из контекстного менеджера."""

    @abstractmethod
    async def upload_file(
        self,
        data: bytes | str | BinaryIO,
        object_name: str,
        content_type: str = "application/octet-stream",
        content_disposition: str | None = None,
    ) -> str:
        """Загрузить файл в хранилище."""

    @abstractmethod
    async def download_file(self, object_name: str) -> bytes:
        """Скачать файл из хранилища."""


class S3StorageService(StorageService):
    """Сервис для работы с S3-совместимым хранилищем."""

    def __init__(self, settings: S3Settings) -> None:
        self.settings = settings
        self._client: Any = None
        self._exit_stack: AsyncExitStack | None = None

    async def __aenter__(self) -> "S3StorageService":
        self._exit_stack = AsyncExitStack()
        s3_config = AioConfig(
            max_pool_connections=self.settings.max_pool_connections,
            connect_timeout=self.settings.connect_timeout,
            read_timeout=self.settings.read_timeout,
        )
        s3_session = Session(
            aws_access_key_id=self.settings.access_key.get_secret_value(),
            aws_secret_access_key=self.settings.secret_key.get_secret_value(),
        )
        client_context = s3_session.client(
            "s3",
            endpoint_url=self.settings.endpoint_url,
            config=s3_config,
        )
        self._client = await self._exit_stack.enter_async_context(client_context)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._exit_stack:
            await self._exit_stack.aclose()
            self._exit_stack = None
            self._client = None

    async def upload_file(
        self,
        data: bytes | str | BinaryIO,
        object_name: str,
        content_type: str = "application/octet-stream",
        content_disposition: str | None = None,
    ) -> str:
        if self._client is None:
            raise RuntimeError("S3 client is not initialized. Use async context manager.")

        extra_args = {"ContentType": content_type}
        if content_disposition:
            extra_args["ContentDisposition"] = content_disposition

        await self._client.put_object(
            Bucket=self.settings.bucket_name,
            Key=object_name,
            Body=data,
            **extra_args,
        )

        url = furl.furl(self.settings.endpoint_url)
        url.path.add(self.settings.bucket_name)
        url.path.add(object_name)
        return str(url)

    async def download_file(self, object_name: str) -> bytes:
        if self._client is None:
            raise RuntimeError("S3 client is not initialized. Use async context manager.")

        response = await self._client.get_object(
            Bucket=self.settings.bucket_name,
            Key=object_name,
        )
        return await response["Body"].read()


class FileSystemStorageService(StorageService):
    """Сервис для работы с файловой системой."""

    def __init__(self, base_path: str | Path) -> None:
        self.base_path = Path(base_path)

    async def __aenter__(self) -> "FileSystemStorageService":
        self.base_path.mkdir(parents=True, exist_ok=True)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    async def upload_file(
        self,
        data: bytes | str | BinaryIO,
        object_name: str,
        content_type: str = "application/octet-stream",
        content_disposition: str | None = None,
    ) -> str:
        file_path = self.base_path / object_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, str):
            data = data.encode("utf-8")

        async with aiofiles.open(file_path, "wb") as f:
            if isinstance(data, bytes):
                await f.write(data)
            else:
                await f.write(data.read())

        return str(file_path)

    async def download_file(self, object_name: str) -> bytes:
        file_path = self.base_path / object_name
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()
