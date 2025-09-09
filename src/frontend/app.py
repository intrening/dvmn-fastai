from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend_files"
FRONTEND_SETTINGS_JSON = "frontend-settings.json"
ASSETS_DIR = FRONTEND_DIR / "assets"


def create_frontend_app() -> FastAPI:
    app = FastAPI()

    @app.get("/frontend-settings.json")
    async def frontend_settings() -> Response:
        return FileResponse(path=str(FRONTEND_SETTINGS_JSON), media_type="application/json")

    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")

    return app
