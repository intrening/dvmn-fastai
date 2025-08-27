from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

api_router = APIRouter(prefix="/frontend-api")


@api_router.get("/hello")
async def hello():
    return {"message": "Привет из бекенда!"}


app = FastAPI()
app.include_router(api_router)


@app.get("/frontend-settings.json")
async def frontend_settings():
    return FileResponse("frontend-settings.json", media_type="application/json")


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
