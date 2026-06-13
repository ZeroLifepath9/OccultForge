"""Persist and version natal overviews so clients always get current copy."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import NatalOverview
from app.services.imprint_overview import build_imprint_overview
from app.services.priest_overview import CHART_MARKER, OVERVIEW_FORMAT
from app.services.interpretations.zero_overview import READING_ENGINE, SEAL_CLOSE, ZERO_OVERVIEW_MARKER

THRESHOLD_MARKER = SEAL_CLOSE
TABLET_FORMAT = OVERVIEW_FORMAT
LEGACY_OVERVIEW_MARKERS = (
    "East:",
    "West:",
    "PRIEST'S READING",
    "What this means for you",
    "the tablet is opened",
    "Phoenix Oracle",
    "Archetype called:",
    "I have kept this gate",
    "THE CHART ·",
    "book report",
    "THE SHORT VERSION",
    "WHO YOU ARE — plain",
    "WHAT ALIGNS WITH YOU",
    "The Humanitarian",
    "humanitarian",
    "YOUR NUMBER IN THIS CURRENT (occult wave)",
    "plain-daily",
    "THE INITIATION",
    "THE SKY PRESSED ON YOUR SEAL",
    "CAREER & BUSINESS",
    "book report",
    "Act I —",
    "BOOK REPORT",
)
REQUIRED_READING_MARKERS = (
    ZERO_OVERVIEW_MARKER,
    "you are",
)
DEEP_READING_ENGINE = READING_ENGINE
FORBIDDEN_READING_PHRASES = (
    "look up",
    "investigate",
    "Occult seeds",
    "Lookup seeds",
    "Lookup:",
    "THE SHORT VERSION",
    "The Humanitarian",
    "THE INITIATION",
)
MAX_THRESHOLD_WORDS = 900
MIN_THRESHOLD_WORDS = 120
MIN_INTERP_WORDS = 120


def _calendar_year() -> int:
    return datetime.utcnow().year


def _cached_overview_stale(cached: dict[str, Any], *, version: str, fingerprint: str) -> str | None:
    if cached.get("content_version") != version:
        return "content_version"
    if cached.get("template_signature") != settings.overview_template_signature:
        return "template_signature"
    if cached.get("reading_kind") != "threshold_seal":
        return "reading_kind"
    facts = cached.get("facts") or {}
    uy = facts.get("universal_year") or {}
    if uy.get("calendar_year") != _calendar_year():
        return "calendar_year"
    if cached.get("overview_format") != TABLET_FORMAT:
        return "overview_format"
    if cached.get("reading_engine") != DEEP_READING_ENGINE:
        return "reading_engine"
    chart = (cached.get("chart_reference") or "").strip()
    interp = (cached.get("interpretation") or "").strip()
    narrative = (cached.get("narrative") or cached.get("deterministic_fallback") or "").strip()
    forge_markers = (CHART_MARKER, "OCCULT FORGE")
    if not any(m in chart or m in narrative for m in forge_markers):
        return "chart_marker"
    if ZERO_OVERVIEW_MARKER not in interp and ZERO_OVERVIEW_MARKER not in narrative:
        return "interpretation_marker"
    for req in REQUIRED_READING_MARKERS:
        if req not in interp and req not in narrative:
            return "reading_engine"
    if THRESHOLD_MARKER not in (interp + narrative).lower():
        return "narrative_format"
    blob = f"{narrative} {interp}"
    if any(m in blob for m in LEGACY_OVERVIEW_MARKERS):
        return "legacy_format"
    if any(p in blob.lower() for p in FORBIDDEN_READING_PHRASES):
        return "forbidden_phrase"
    if not cached.get("natal_chart_record") and not facts.get("natal_chart_record"):
        return "chart_record"
    words = len(narrative.split())
    if words > MAX_THRESHOLD_WORDS:
        return "narrative_long"
    if len(interp.split()) < MIN_INTERP_WORDS:
        return "interpretation_short"
    if words < MIN_THRESHOLD_WORDS:
        return "narrative_short"
    return None


async def get_or_build_overview(
    *,
    user_id: str,
    imprint: dict[str, Any],
    db: AsyncSession,
    force: bool = False,
) -> dict[str, Any]:
    version = settings.overview_content_version
    fingerprint = imprint["birth_fingerprint"]

    if not force:
        result = await db.execute(
            select(NatalOverview).where(NatalOverview.user_id == user_id)
        )
        row = result.scalar_one_or_none()
        if row and row.birth_fingerprint == fingerprint:
            cached = json.loads(row.overview_json)
            stale_reason = _cached_overview_stale(
                cached, version=version, fingerprint=fingerprint
            )
            if not stale_reason and row.content_version == version:
                cached["cached"] = True
                return cached

    overview = await build_imprint_overview(imprint, use_ai=False)
    overview["content_version"] = version
    overview["template_signature"] = settings.overview_template_signature
    overview["cached"] = False
    overview["generated_at"] = datetime.utcnow().isoformat() + "Z"
    overview["calendar_year"] = _calendar_year()

    result = await db.execute(
        select(NatalOverview).where(NatalOverview.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    payload = json.dumps(overview, ensure_ascii=False)
    if row:
        row.birth_fingerprint = fingerprint
        row.content_version = version
        row.overview_json = payload
        row.updated_at = datetime.utcnow()
    else:
        db.add(
            NatalOverview(
                user_id=user_id,
                birth_fingerprint=fingerprint,
                content_version=version,
                overview_json=payload,
            )
        )
    await db.commit()
    return overview


async def delete_overview(user_id: str, db: AsyncSession) -> None:
    result = await db.execute(
        select(NatalOverview).where(NatalOverview.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if row:
        await db.delete(row)
        await db.commit()