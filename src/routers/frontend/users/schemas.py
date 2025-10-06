from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt
from pydantic.alias_generators import to_camel

UserName = Annotated[
    str,
    Field(
        max_length=254,
        examples=["ivan", "alex123"],
    ),
]


class UserDetailsResponse(BaseModel):
    """Информация о текущем пользователе"""

    email: EmailStr = Field(description="Email пользователя")
    is_active: bool = Field(description="Активен ли пользователь")
    profile_id: PositiveInt = Field(description="ID профиля пользователя")
    registered_at: datetime = Field(description="Дата регистрации пользователя")
    updated_at: datetime = Field(description="Дата обновления профиля пользователя")
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


__all__ = [
    "UserName",
    "UserDetailsResponse",
]
