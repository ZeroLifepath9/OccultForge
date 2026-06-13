import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from app.api import (
    account_router,
    auth_router,
    imprint_router,
    location_router,
    reflection_router,
    zero_router,
)
from app.config import settings, validate_production_settings
from app.database import init_db


def _health_payload() -> dict:
    from app.config import production_config_status

    return {
        "status": "ok",
        "phase": "5-auth",
        "env": settings.env,
        "xai_configured": bool(settings.xai_api_key),
        "paid_dev_unlock": settings.paid_dev_unlock,
        "deploy": os.environ.get("RENDER_GIT_COMMIT", "local")[:12],
        "frontend_build": _frontend_build_stamp(),
        "config": production_config_status(),
    }

def _static_dir() -> Path:
    app_dir = Path(__file__).resolve().parent
    for candidate in (
        app_dir.parent / "frontend" / "public",  # flat: repo/app → repo/frontend
        app_dir.parent.parent / "frontend" / "public",  # repo/backend/app → repo/frontend
        app_dir.parent.parent.parent / "frontend" / "public",
    ):
        if candidate.is_dir():
            return candidate
    return app_dir.parent.parent / "frontend" / "public"


STATIC_DIR = _static_dir()


def _frontend_build_stamp() -> str:
    stamp = STATIC_DIR / "BUILD.txt"
    try:
        if stamp.is_file():
            return stamp.read_text(encoding="utf-8").strip()[:64]
    except OSError:
        pass
    return "unknown"


class NoCacheStaticFiles(StaticFiles):
    """Serve JS/CSS without long-lived browser cache — query bumps alone are not enough."""

    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 200:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
        return response


@asynccontextmanager
async def lifespan(_: FastAPI):
    validate_production_settings()
    await init_db()
    yield


_docs_url = None if settings.is_production else "/docs"
_redoc_url = None if settings.is_production else "/redoc"

app = FastAPI(
    title="Occult Forge",
    description="Birth imprint: BaZi, Vedic, Western, multi-school numerology",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=_docs_url,
    redoc_url=_redoc_url,
    openapi_url=None if settings.is_production else "/openapi.json",
)

_origins = settings.cors_origin_list()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins if _origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(imprint_router)
app.include_router(reflection_router)
app.include_router(zero_router)
app.include_router(location_router)
app.include_router(account_router)


@app.get("/health")
async def health():
    return _health_payload()


@app.get("/healthz")
async def healthz():
    """Render default health check path is /healthz."""
    return _health_payload()


if STATIC_DIR.exists():
    app.mount("/static", NoCacheStaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    async def index():
        index_file = STATIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(
                index_file,
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                },
            )
        return {"message": "Occult Chart API — visit /docs"}

    @app.get("/mockup")
    async def mobile_mockup():
        mockup_file = STATIC_DIR / "mobile-mockup.html"
        if mockup_file.exists():
            return FileResponse(
                mockup_file,
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                },
            )
        return {"message": "Mockup not found"}