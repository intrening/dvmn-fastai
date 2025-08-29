from fastapi import APIRouter, FastAPI

from .apps.frontend import create_frontend_app

api_router = APIRouter(prefix="/frontend-api")


@api_router.get("/hello")
async def hello():
    return {"message": "Привет из бекенда!"}


app = FastAPI()
app.include_router(api_router)


frontend_app = create_frontend_app()
app.mount("/", frontend_app)
