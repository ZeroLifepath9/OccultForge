"""Load curated location / company knowledge bases."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent


@lru_cache
def load_states() -> list[dict]:
    return json.loads((KB_DIR / "us_states.json").read_text(encoding="utf-8"))


@lru_cache
def load_cities() -> list[dict]:
    return json.loads((KB_DIR / "cities.json").read_text(encoding="utf-8"))


@lru_cache
def load_companies() -> list[dict]:
    return json.loads((KB_DIR / "companies.json").read_text(encoding="utf-8"))


def state_by_code(code: str) -> dict | None:
    code = code.upper()
    return next((s for s in load_states() if s["code"] == code), None)


def city_by_name(name: str) -> dict | None:
    key = name.strip().lower()
    return next((c for c in load_cities() if c["name"].lower() == key), None)


def companies_for_state(state_code: str, limit: int = 8) -> list[dict]:
    code = state_code.upper()
    return [c for c in load_companies() if c.get("hq_state") == code][:limit]


def companies_for_city(city_name: str, limit: int = 6) -> list[dict]:
    key = city_name.strip().lower()
    return [
        c for c in load_companies()
        if c.get("hq_city", "").lower() == key
    ][:limit]