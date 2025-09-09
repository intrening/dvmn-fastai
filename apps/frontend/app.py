from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

SRC_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = SRC_DIR.parent
FRONTEND_DIR = SRC_DIR / "apps/frontend/frontend"
FRONTEND_SETTINGS_JSON = PROJECT_ROOT / "frontend-settings.json"


def create_frontend_app() -> FastAPI:
    app = FastAPI()

    @app.get("/frontend-settings.json")
    async def frontend_settings() -> Response:
        return FileResponse(path=str(FRONTEND_SETTINGS_JSON), media_type="application/json")

    assets_dir = str(FRONTEND_DIR / "assets")
    static_dir = str(FRONTEND_DIR)

    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

    return app
