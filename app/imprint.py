"""Orchestrates full birth imprint computation."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from app.config import settings


def birth_fingerprint(
    birth_local: datetime,
    timezone: str,
    latitude: float,
    longitude: float,
    display_name: str,
) -> str:
    payload = json.dumps(
        {
            "birth": birth_local.isoformat(),
            "tz": timezone,
            "lat": latitude,
            "lon": longitude,
            "name": display_name.strip().lower(),
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def local_to_utc(birth_local: datetime, timezone: str) -> datetime:
    if birth_local.tzinfo is None:
        tz = ZoneInfo(timezone)
        birth_local = birth_local.replace(tzinfo=tz)
    return birth_local.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)


def compute_imprint(
    display_name: str,
    birth_datetime_local: datetime,
    timezone: str,
    latitude: float,
    longitude: float,
    birth_place_label: str = "",
    commonly_known_as: str | None = None,
    gender: str = "male",
) -> dict[str, Any]:
    from app.calculators import compute_bazi, compute_numerology, compute_vedic, compute_western

    birth_utc = local_to_utc(birth_datetime_local, timezone)
    fingerprint = birth_fingerprint(
        birth_datetime_local, timezone, latitude, longitude, display_name
    )

    numerology = compute_numerology(display_name, birth_datetime_local)
    if commonly_known_as and commonly_known_as.strip():
        numerology["commonly_known_as"] = compute_numerology(
            commonly_known_as.strip(), birth_datetime_local
        )["schools"]["pythagorean"]

    return {
        "schema_version": settings.imprint_schema_version,
        "computed_at": datetime.utcnow().isoformat() + "Z",
        "birth_fingerprint": fingerprint,
        "birth": {
            "name": display_name,
            "display_name": display_name,
            "commonly_known_as": commonly_known_as or "",
            "datetime_local": birth_datetime_local.isoformat(),
            "datetime_utc": birth_utc.isoformat() + "Z",
            "timezone": timezone,
            "latitude": latitude,
            "longitude": longitude,
            "place": birth_place_label,
            "gender": "female" if gender == "female" else "male",
        },
        "numerology": numerology,
        "bazi": compute_bazi(birth_datetime_local, gender=gender),
        "western": compute_western(birth_utc, latitude, longitude),
        "vedic": compute_vedic(
            birth_utc, latitude, longitude, ayanamsa=settings.vedic_ayanamsa
        ),
    }