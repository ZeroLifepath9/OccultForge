import os
import secrets
import sys
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEV_JWT = "dev-only-change-in-production"
_SECRET_FILE_CANDIDATES = (
    "JWT_SECRET",
    "/etc/secrets/JWT_SECRET",
    "/run/secrets/JWT_SECRET",
)


def _env_value(*names: str) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def _read_secret_file() -> str:
    for candidate in _SECRET_FILE_CANDIDATES:
        path = Path(candidate)
        if not path.is_file():
            continue
        try:
            value = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if value:
            return value
    return ""


def _valid_jwt(secret: str) -> bool:
    return bool(secret) and secret != _DEV_JWT and len(secret) >= 32


def resolve_jwt_secret() -> tuple[str, str]:
    """Return (secret, source) where source is env|file|ephemeral|dev."""
    for source, value in (
        ("env", _env_value("JWT_SECRET")),
        ("file", _read_secret_file()),
    ):
        if _valid_jwt(value):
            return value, source
    if _env_value("ENV").lower() in ("production", "prod") or os.environ.get("RENDER"):
        ephemeral = secrets.token_urlsafe(48)
        return ephemeral, "ephemeral"
    return _DEV_JWT, "dev"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
    )

    env: str = Field(default="development", validation_alias="ENV")
    database_url: str = "sqlite+aiosqlite:///./occult_chart.db"
    imprint_schema_version: str = "1.0.0"
    vedic_ayanamsa: str = "lahiri"

    # xAI — create key at https://console.x.ai/team/.../api-keys
    xai_api_key: str = Field(default="", validation_alias="XAI_API_KEY")
    xai_base_url: str = "https://api.x.ai/v1"
    xai_model_daily: str = "grok-3-mini-fast"
    xai_model_zero: str = "grok-4"

    # Paid location insights: true = all users get paid APIs (local dev only)
    paid_dev_unlock: bool = True

    # Auth — required in production (min 32 chars)
    jwt_secret: str = Field(default=_DEV_JWT, validation_alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    # Comma-separated origins, e.g. https://occult-forge.onrender.com
    cors_origins: str = Field(default="", validation_alias="CORS_ORIGINS")

    overview_content_version: str = "29"
    overview_template_signature: str = "zero-overview"
    overview_require_ai: bool = False

    @property
    def is_production(self) -> bool:
        return self.env.strip().lower() in ("production", "prod")

    def cors_origin_list(self) -> list[str]:
        raw = [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        if raw:
            return raw
        if self.is_production:
            render_url = _env_value("RENDER_EXTERNAL_URL").rstrip("/")
            if render_url:
                return [render_url]
            return []
        return ["*"]

    @field_validator("paid_dev_unlock")
    @classmethod
    def no_paid_unlock_in_prod(cls, v: bool, info) -> bool:
        env = (info.data.get("env") or "development").strip().lower()
        if env in ("production", "prod") and v:
            return False
        return v

    @model_validator(mode="after")
    def apply_process_env(self) -> "Settings":
        """Render injects env vars at runtime; overlay anything pydantic missed."""
        env = _env_value("ENV")
        if env:
            self.env = env
        jwt = _env_value("JWT_SECRET")
        if jwt:
            self.jwt_secret = jwt
        xai = _env_value("XAI_API_KEY")
        if xai:
            self.xai_api_key = xai
        cors = _env_value("CORS_ORIGINS")
        if cors:
            self.cors_origins = cors
        return self


settings = Settings()


def production_config_status() -> dict[str, str]:
    jwt = settings.jwt_secret
    cors = settings.cors_origin_list()
    render_url = _env_value("RENDER_EXTERNAL_URL")
    return {
        "env": settings.env,
        "jwt_secret": "ok" if _valid_jwt(jwt) else "MISSING",
        "jwt_length": str(len(jwt)),
        "cors_origins": "set" if cors else "MISSING",
        "render_external_url": render_url or "not set",
        "xai_api_key": "set" if (_env_value("XAI_API_KEY") or settings.xai_api_key) else "not set",
    }


def validate_production_settings() -> None:
    if not settings.is_production:
        return

    jwt, jwt_source = resolve_jwt_secret()
    settings.jwt_secret = jwt

    if not settings.cors_origin_list():
        render_url = _env_value("RENDER_EXTERNAL_URL").rstrip("/")
        if render_url:
            settings.cors_origins = render_url

    status = production_config_status()
    status["jwt_source"] = jwt_source
    print(
        "[occult-forge] startup config: "
        + ", ".join(f"{k}={v}" for k, v in status.items()),
        flush=True,
    )

    if jwt_source == "ephemeral":
        print(
            "[occult-forge] WARNING: JWT_SECRET not set in Render → Environment. "
            "Using a temporary secret for this deploy only (logins reset on restart). "
            "Add JWT_SECRET with 48+ random characters, Save Changes, redeploy.",
            file=sys.stderr,
            flush=True,
        )

    if not settings.cors_origin_list():
        print(
            "[occult-forge] WARNING: CORS_ORIGINS unset and RENDER_EXTERNAL_URL missing. "
            "Add CORS_ORIGINS=https://occultforge.onrender.com in Render → Environment.",
            file=sys.stderr,
            flush=True,
        )