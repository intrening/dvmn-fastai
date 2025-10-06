from fastapi import APIRouter

from .schemas import UserDetailsResponse
from ..mocks import get_mock_user_details_response

router = APIRouter(tags=["Users"])


@router.get(
    "/users/me",
    response_model=UserDetailsResponse,
    summary="Получить информацию о текущем пользователе",
    description="Возвращает данные профиля текущего авторизованного пользователя.",
)
async def me() -> UserDetailsResponse:
    return get_mock_user_details_response()


__all__ = ["router"]
