from datetime import datetime

from .users.schemas import UserDetailsResponse


def get_mock_user_details_response() -> UserDetailsResponse:
    return UserDetailsResponse(
        email="example@example.com",
        is_active=True,
        profile_id=1,
        registered_at=datetime(2025, 6, 15, 18, 29, 56),
        updated_at=datetime(2025, 6, 15, 18, 29, 56),
        username="user123",
    )
