"""Match Occult KB rituals to chart context tags."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_KB_PATH = Path(__file__).resolve().parent.parent / "kb" / "rituals.json"


def _load_rituals() -> list[dict[str, Any]]:
    if not _KB_PATH.exists():
        return []
    return json.loads(_KB_PATH.read_text(encoding="utf-8"))


def ritual_candidates_for_payload(payload: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
    """Select rituals by element / dasha lord tags."""
    bazi = payload.get("bazi", {})
    vedic = payload.get("vedic") or {}
    day_master = imprint_element_hint(bazi.get("day_master", ""))

    tags = set()
    if day_master:
        tags.add(f"element:{day_master.lower()}")
    lord = vedic.get("active_mahadasha_lord", "")
    if lord:
        tags.add(f"planet:{lord.lower()}")

    matches = []
    for entry in _load_rituals():
        entry_tags = set(entry.get("tags", []))
        if tags & entry_tags:
            matches.append(entry)
    return matches[:limit]


def imprint_element_hint(stem: str) -> str:
    mapping = {
        "甲": "wood", "乙": "wood",
        "丙": "fire", "丁": "fire",
        "戊": "earth", "己": "earth",
        "庚": "metal", "辛": "metal",
        "壬": "water", "癸": "water",
    }
    return mapping.get(stem, "")