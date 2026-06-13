"""Vedic sidereal chart + simplified Vimshottari Dasha."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import swisseph as swe

from app.calculators.western import PLANETS, SIGNS, _sign_from_longitude, _to_jd

# Vimshottari: nakshatra lords cycle, years per lord
DASHA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]
NAKSHATRA_SPAN = 360 / 27  # 13°20'

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshta",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]


def _nakshatra(moon_lon: float) -> dict[str, Any]:
    idx = int(moon_lon // NAKSHATRA_SPAN) % 27
    fraction = (moon_lon % NAKSHATRA_SPAN) / NAKSHATRA_SPAN
    pada = int(fraction * 4) + 1
    lord = DASHA_LORDS[idx % 9]
    return {
        "name": NAKSHATRA_NAMES[idx],
        "index": idx + 1,
        "pada": min(pada, 4),
        "lord": lord,
    }


def _vimshottari_tree(birth_utc: datetime, moon_lon: float) -> dict[str, Any]:
    """Build Maha Dasha periods from Moon nakshatra lord."""
    idx = int(moon_lon // NAKSHATRA_SPAN) % 27
    birth_lord = DASHA_LORDS[idx % 9]
    lord_index = DASHA_LORDS.index(birth_lord)

    # Balance of first dasha: fraction remaining in nakshatra
    pos_in_nak = moon_lon % NAKSHATRA_SPAN
    fraction_remaining = 1 - (pos_in_nak / NAKSHATRA_SPAN)
    first_years = DASHA_YEARS[lord_index] * fraction_remaining

    periods = []
    start = birth_utc
    end = start + timedelta(days=first_years * 365.25)
    periods.append({
        "lord": birth_lord,
        "level": "mahadasha",
        "start": start.isoformat(),
        "end": end.isoformat(),
        "years": round(first_years, 2),
    })

    current = end
    for i in range(1, 9):
        li = (lord_index + i) % 9
        lord = DASHA_LORDS[li]
        years = DASHA_YEARS[li]
        end = current + timedelta(days=years * 365.25)
        periods.append({
            "lord": lord,
            "level": "mahadasha",
            "start": current.isoformat(),
            "end": end.isoformat(),
            "years": years,
        })
        current = end

    active = next(
        (p for p in periods if p["start"] <= datetime.utcnow().isoformat() <= p["end"]),
        periods[0],
    )
    return {
        "birth_nakshatra_lord": birth_lord,
        "mahadasha_periods": periods,
        "active_mahadasha": active,
    }


def _house_from_lagna(planet_lon: float, lagna_lon: float) -> int:
    diff = (planet_lon - lagna_lon) % 360
    return int(diff // 30) + 1


def compute_vedic(
    birth_utc: datetime,
    latitude: float,
    longitude: float,
    ayanamsa: str = "lahiri",
) -> dict[str, Any]:
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = _to_jd(birth_utc)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    bodies: dict[str, Any] = {}
    moon_lon = 0.0
    for name, pid in PLANETS:
        xx, _ = swe.calc_ut(jd, pid, flags)
        lon = xx[0] % 360
        if name == "Moon":
            moon_lon = lon
        bodies[name] = {
            "longitude": round(lon, 4),
            **_sign_from_longitude(lon),
        }

    # Whole-sign style lagna from sidereal ascendant
    cusps, _ = swe.houses_ex(jd, latitude, longitude, b"W", flags)
    lagna_lon = cusps[1] % 360 if len(cusps) > 1 else 0.0
    lagna = _sign_from_longitude(lagna_lon)

    houses = []
    for h in range(1, 13):
        sign_idx = (int(lagna_lon // 30) + h - 1) % 12
        houses.append({
            "house": h,
            "sign": SIGNS[sign_idx],
            "planets": [
                n for n, b in bodies.items()
                if _house_from_lagna(b["longitude"], lagna_lon) == h
            ],
        })

    nak = _nakshatra(moon_lon)
    dasha = _vimshottari_tree(birth_utc, moon_lon)

    return {
        "zodiac": "sidereal",
        "ayanamsa": ayanamsa,
        "lagna": lagna,
        "planets": bodies,
        "houses": houses,
        "moon_nakshatra": nak,
        "dasha": dasha,
    }