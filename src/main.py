from fastapi import FastAPI

from .core.config import AppSettings
from .frontend import create_frontend_app
from .frontend_api.app import api_router as frontend_api_router

settings = AppSettings()


app = FastAPI(debug=settings.debug)
app.include_router(frontend_api_router)

frontend_app = create_frontend_app()
app.mount("/", frontend_app)
