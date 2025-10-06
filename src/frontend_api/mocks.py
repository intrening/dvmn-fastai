from datetime import datetime

from furl import furl

from src.core.config import settings
from src.frontend_api.sites.schemas import CreateSiteRequest, GeneratedSiteResponse, SiteResponse

from .users.schemas import UserDetailsResponse

MOCK_SITE_ID = 1
MOCK_TITLE = "Тестовый сайт"
MOCK_PROMPT = "Тестовый промпт для сайта"
MOCK_SITE_HTML_FILE_NAME = "mocked_site.html"
MOCK_SITE_SCREENSHOT_FILE_NAME = "mocked_site.png"
MOCK_CREATED_AT = datetime(2025, 6, 15, 18, 29, 56)
MOCK_UPDATED_AT = datetime(2025, 6, 15, 18, 29, 56)


def get_mock_site_html_file_url(is_download: bool = False) -> str:
    html_file_url = furl(settings.s3.endpoint_url)
    html_file_url.path.add(settings.s3.bucket_name)
    html_file_url.path.add(MOCK_SITE_HTML_FILE_NAME)
    html_file_url.args["response-content-disposition"] = "inline" if not is_download else "attachment"
    return html_file_url.url


def get_mock_screenshot_url() -> str:
    screenshot_file_url = furl(settings.s3.endpoint_url)
    screenshot_file_url.path.add(settings.s3.bucket_name)
    screenshot_file_url.path.add(MOCK_SITE_SCREENSHOT_FILE_NAME)
    return screenshot_file_url.url


def get_mock_user_details_response() -> UserDetailsResponse:
    return UserDetailsResponse(
        email="example@example.com",
        is_active=True,
        profile_id=1,
        registered_at=datetime(2025, 6, 15, 18, 29, 56),
        updated_at=datetime(2025, 6, 15, 18, 29, 56),
        username="user123",
    )


def get_mock_generated_site_response(request: CreateSiteRequest) -> GeneratedSiteResponse:
    return GeneratedSiteResponse(
        id=MOCK_SITE_ID,
        title=MOCK_TITLE,
        prompt=request.prompt,
        screenshot_url=get_mock_screenshot_url(),
        html_code_url=get_mock_site_html_file_url(),
        html_code_download_url=get_mock_site_html_file_url(is_download=True),
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )


def get_mock_site_response() -> SiteResponse:
    return SiteResponse(
        id=MOCK_SITE_ID,
        title=MOCK_TITLE,
        prompt=MOCK_PROMPT,
        screenshot_url=get_mock_screenshot_url(),
        html_code_url=get_mock_site_html_file_url(),
        html_code_download_url=get_mock_site_html_file_url(is_download=True),
        created_at=MOCK_CREATED_AT,
        updated_at=MOCK_UPDATED_AT,
    )
