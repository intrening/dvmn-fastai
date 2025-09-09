from datetime import datetime

from fastapi import APIRouter

from .schemas import UserDetailsResponse

router = APIRouter(tags=["Users"])


@router.get(
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


__all__ = ["router"]
