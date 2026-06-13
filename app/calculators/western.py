"""Western tropical natal chart via Swiss Ephemeris."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import swisseph as swe

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

PLANETS = [
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mercury", swe.MERCURY),
    ("Venus", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Uranus", swe.URANUS),
    ("Neptune", swe.NEPTUNE),
    ("Pluto", swe.PLUTO),
]


def _to_jd(dt: datetime) -> float:
    ut = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    return swe.julday(dt.year, dt.month, dt.day, ut)


def _sign_from_longitude(lon: float) -> dict[str, Any]:
    lon = lon % 360
    idx = int(lon // 30)
    return {
        "sign": SIGNS[idx],
        "degree": round(lon % 30, 4),
        "absolute_longitude": round(lon, 4),
    }


def _local_sidereal_time(jd: float, longitude: float) -> float:
    return swe.sidtime(jd) + longitude / 15.0


def _placidus_cusps(jd: float, latitude: float, longitude: float) -> list[float]:
    cusps, ascmc = swe.houses(jd, latitude, longitude, b"P")
    return list(cusps)


def compute_western(
    birth_utc: datetime,
    latitude: float,
    longitude: float,
) -> dict[str, Any]:
    jd = _to_jd(birth_utc)
    swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)  # tropical default reset
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    bodies: dict[str, Any] = {}
    for name, pid in PLANETS:
        xx, _ = swe.calc_ut(jd, pid, flags)
        bodies[name] = {
            "longitude": round(xx[0], 4),
            "speed": round(xx[3], 4),
            **_sign_from_longitude(xx[0]),
        }

    cusps = _placidus_cusps(jd, latitude, longitude)
    houses = []
    for i in range(1, 13):
        lon = cusps[i] if i < len(cusps) else cusps[i - 1]
        houses.append({
            "house": i,
            **_sign_from_longitude(lon),
        })

    asc_lon = cusps[1] if len(cusps) > 1 else 0.0
    mc_lon = cusps[10] if len(cusps) > 10 else 0.0

    return {
        "zodiac": "tropical",
        "house_system": "Placidus",
        "planets": bodies,
        "houses": houses,
        "angles": {
            "ascendant": _sign_from_longitude(asc_lon),
            "midheaven": _sign_from_longitude(mc_lon),
        },
        "julian_day": jd,
    }