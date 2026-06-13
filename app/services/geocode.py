"""Resolve Place of Birth to coordinates and IANA timezone."""

from __future__ import annotations

from typing import Any

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


async def geocode_place(place: str) -> dict[str, Any]:
    place = place.strip()
    if len(place) < 2:
        raise ValueError("Place of Birth is too short")

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            NOMINATIM_URL,
            params={"q": place, "format": "json", "limit": 1, "addressdetails": 1},
            headers={"User-Agent": "OccultForge/1.0 (birth-chart-app)"},
        )
        response.raise_for_status()
        results = response.json()

    if not results:
        raise ValueError(f"Could not find a location for: {place}")

    hit = results[0]
    lat = float(hit["lat"])
    lon = float(hit["lon"])
    display = hit.get("display_name", place)

    timezone = _timezone_at(lat, lon)
    if not timezone:
        raise ValueError(f"Could not determine timezone for: {place}")

    return {
        "place": place,
        "display_name": display,
        "latitude": lat,
        "longitude": lon,
        "timezone": timezone,
    }


def _timezone_at(lat: float, lon: float) -> str | None:
    try:
        from timezonefinder import TimezoneFinder

        tf = TimezoneFinder()
        return tf.timezone_at(lat=lat, lng=lon)
    except ImportError:
        pass
    # Fallback: coarse US-centric guess (install timezonefinder for accuracy)
    if 24 <= lat <= 50 and -125 <= lon <= -66:
        return "America/New_York"
    if 40 <= lat <= 60 and -10 <= lon <= 40:
        return "Europe/London"
    return "UTC"