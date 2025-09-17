import asyncio
import mimetypes

import aioboto3
from aioboto3.session import AioConfig
from furl import furl

BUCKET_NAME = "testbucket"


async def main() -> None:
    filename = "index.html"
    mime_type, _ = mimetypes.guess_type(filename)

    config = AioConfig(
        max_pool_connections=10,
        connect_timeout=10,
        read_timeout=30,
    )

    minio_endpoint = "http://localhost:9000"
    minio_access_key = "minioadmin"
    minio_secret_key = "minioadmin"

    with open(filename, "rb") as file:
        html_content = file.read()

    upload_params = {
        "Bucket": BUCKET_NAME,
        "Key": filename,
        "Body": html_content,
        "ContentType": mime_type,
        "ContentDisposition": "inline",
    }

    session = aioboto3.Session(
        aws_access_key_id=minio_access_key,
        aws_secret_access_key=minio_secret_key,
    )
    async with session.client(
        "s3",
        endpoint_url=minio_endpoint,
        config=config,
    ) as s3_client:
        await s3_client.put_object(**upload_params)
    print("Файл успешно загружен в MinIO.")

    file_url = furl(minio_endpoint)
    file_url.path.add(BUCKET_NAME)
    file_url.path.add(filename)
    file_url.args["response-content-disposition"] = "inline"
    print("Ссылка")
    print(file_url.url)


if __name__ == "__main__":
    asyncio.run(main())
