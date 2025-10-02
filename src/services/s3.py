import logging
from contextlib import AsyncExitStack
from typing import Any, BinaryIO, Optional

import furl
from aioboto3.session import AioConfig, Session

from ..core.config import S3Settings

logger = logging.getLogger(__name__)


class S3Service:
    """S3 storage service for file operations."""

    def __init__(self, settings: S3Settings) -> None:
        self.settings = settings
        self._client: Any = None
        self._exit_stack: Optional[AsyncExitStack] = None

    async def connect(self) -> None:
        """Connect to S3 service."""
        if self._client is not None:
            logger.warning("S3 client already connected")
            return

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

    async def disconnect(self) -> None:
        """Disconnect from S3 service."""
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
            self._exit_stack = None
            self._client = None

    async def __aenter__(self) -> "S3Service":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.disconnect()

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
