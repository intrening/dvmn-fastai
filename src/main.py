from fastapi import APIRouter, FastAPI

from .apps.frontend import create_frontend_app

api_router = APIRouter(prefix="/frontend-api")


@api_router.get("/hello")
async def hello():
    return {"message": "Привет из бекенда!"}


@api_router.get("/users/me")
async def me():
    return {
        "email": "example@example.com",
        "is_active": True,
        "profile_id": "1",
        "registered_at": "2025-06-15T18:29:56+00:00",
        "updated_at": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }


app = FastAPI()
app.include_router(api_router)


frontend_app = create_frontend_app()
app.mount("/", frontend_app)
