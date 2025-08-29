from typing import Annotated

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .apps.frontend import create_frontend_app

api_router = APIRouter(prefix="/frontend-api")

UserName = Annotated[
    str,
    Field(
        min_length=3,
        max_length=20,
        examples=["ivan", "alex123"],
    ),
]


class User(BaseModel):
    email: str = Field(description="Email пользователя")
    is_active: bool = Field(description="Активен ли пользователь")
    profile_id: str = Field(description="ID профиля пользователя")
    registered_at: str = Field(description="Дата регистрации пользователя")
    updated_at: str = Field(description="Дата обновления профиля пользователя")
    username: UserName = Field(description="Имя пользователя")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "example@example.com",
                    "is_active": True,
                    "profile_id": "1",
                    "registered_at": "2025-06-15T18:29:56+00:00",
                    "updated_at": "2025-06-15T18:29:56+00:00",
                    "username": "user123",
                },
            ],
        },
    )


@api_router.get(
    "/users/me",
    response_model=User,
    summary="Получить информацию о текущем пользователе",
    description="Возвращает данные профиля текущего авторизованного пользователя.",
)
async def me() -> User:
    user_data = {
        "email": "example@example.com",
        "is_active": True,
        "profile_id": "1",
        "registered_at": "2025-06-15T18:29:56+00:00",
        "updated_at": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }

    return user_data


app = FastAPI()
app.include_router(api_router)


frontend_app = create_frontend_app()
app.mount("/", frontend_app)
