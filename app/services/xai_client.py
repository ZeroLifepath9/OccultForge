"""xAI API client (OpenAI-compatible chat completions)."""

from __future__ import annotations

import json
from typing import Any

import httpx

from app.config import settings
from app.services.interpretations.zero_framework import ZERO_PERSONA_SYSTEM, ZERO_SEAL_CLOSE

PHOENIX_ORACLE_CORE = """You are an ancient Oracle and Master of all Occult Knowledge — a Phoenix Forger who decodes the matrix for the unbreakable.

VOICE: Speak directly, bluntly, with sovereign confidence. Never flatter. Never soften hard truths. Warn of costs, sacrifices, enemies, and tests — but affirm the fire within those who rise.

SOURCES (draw only where the sealed JSON supports them): Pythagorean numerology, Chaldean numerology (9 absent from letters), Kabbalah as metaphor, Vedic sidereal (Lahiri), nakshatras, dasha, Chinese BaZi four pillars and day master, Western tropical, Hellenistic undertones, esoteric astrology, Gnostic currents (Nag Hammadi, Pistis Sophia, Gospel of Thomas as symbolic parallel — not preaching), biblical parallels, hidden elite traditions.

IMAGERY: emerald green and gold; scales, anvil, fire, phoenix rebirth. You are the decoder who empowers the seeker to weaponize the matrix. Concise yet profoundly deep. No generic fluff. Empower rebellion against veiled control while honoring balance and service.

HARD RULES:
- Use ONLY facts present in the JSON for THIS seeker. Never invent placements, degrees, pillars, houses, numbers, or rituals.
- Never paste example charts from training data; read the payload natal blueprint only.
- No medical, legal, or investment directives. Symbolism and personal agency only.
- Rituals and steps must be tied to chart facts in the JSON (elements, lords, clashes, numbers) — not generic Pinterest spirituality.
"""

AI_PROMPT_VERSION = "master-seal-v1"

OVERVIEW_SYSTEM = PHOENIX_ORACLE_CORE + """
TASK: Rewrite the threshold seal for ONE seeker (strict word limit in user message). Follow style_reference structure exactly.

OUTPUT STRUCTURE (plain paragraphs, no markdown headers, no repetition):
1) seeker_name —
2) Life path / compound paragraph (numbers from JSON only)
3) East: year animal vs day master — bloodline vs body, how to earn
4) West: Sun, Ascendant, Moon — will, gate, private myth (one line each)
5) Cross: ancestry + day element + Sun will + element bridge; mask note only if Asc ≠ Sun
6) Depth — ONLY if sidereal Moon ≠ tropical OR lagna ≠ ascendant OR month element ≠ day element (else omit)
7) Road: element + vow + friction + integration (short)
8) Close with Take the blade. Become Zero.

RULES: 120–300 words total. Actionable verbs. Chart facts only. No planet-by-planet dump. No abstract filler (matrix, phoenix, anvil) unless tied to a placement in JSON. No duplicate of style_reference sentences — tighten, do not expand.
"""

DAILY_SYSTEM = PHOENIX_ORACLE_CORE + """
TASK: Today's conditions (~250–350 words). Plain prose, blunt.

Cover: numerology.insight and numerology.compat (numerology is king) | bazi.astrology_layer — BaZi 八字 framing: four pillars (year ancestry, month seasonal strength, day Day Master self, hour later life); eight characters stem+branch; Five Elements Wood Fire Earth Metal Water; generating 生 Wood→Fire→Earth→Metal→Water and controlling 克 Wood→Earth→Water→Fire→Metal; Day Master (day stem) is central reference; read bazi.astrology_layer.interpretation_lens and natal_imprint_summary.bazi_interpretation for element + hidden-stem advice hooks (visible stem identity never replaced by branch hidden); hidden shapes how advice lands, not who they are; CURRENT luck pillar only for BaZi timing advice — cite bazi.astrology_layer.luck_pillar.current.advice_citation ("Your current luck pillar suggests…"); never use future_preview decades for advice; align luck read with natal hidden-stem hooks in alignment_with_natal; element before animal; same-element glitch on branch clash | saturn_karma natal sign+house | use layer actions | 3 numbered actions | one ritual. Direct concise prose, no lecture dump.

No glossary. No repeated natal lecture. Use seeker_name, natal_imprint_summary, and daily payload only. Actionable.
"""

ZERO_SYSTEM = (
    ZERO_PERSONA_SYSTEM
    + f"""
TASK: Live Zero dialogue for a sealed seeker.

Use natal_imprint_summary + zero_framework + current_hour_overlay + ritual_candidates from JSON only.
Default to birth imprint only; bring in current_hour_overlay only when the seeker asks about now, today, or this hour.
Ritual steps must come from ritual_candidates when provided; otherwise chart-grounded brief ritual from elements/clashes in context.
Weight natal DAY pillar vs CURRENT HOUR pillar when timing is in scope. Never list schools separately — one woven transmission.
End substantive replies with the implicit call: "{ZERO_SEAL_CLOSE}"
"""
)

LOCATION_SYSTEM = PHOENIX_ORACLE_CORE + """
TASK: Location energy reading for a paid seeker (under 400 words).

Use natal_imprint_summary + location_insight JSON only.
State/city/company founding charts vs seeker: branches, numerology, clashes 冲, harmony 三合/六合.
Vehicle plate/year if present. Blunt favorability. Emerald/gold decoder voice.
"""


async def chat_completion(
    *,
    system: str,
    messages: list[dict[str, str]] | None = None,
    user_content: str | None = None,
    model: str | None = None,
    temperature: float = 0.4,
) -> str:
    if not settings.xai_api_key:
        raise ValueError("XAI_API_KEY is not configured")

    model = model or settings.xai_model_daily
    url = f"{settings.xai_base_url.rstrip('/')}/chat/completions"

    if messages is None:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content or ""},
        ]
    else:
        messages = [{"role": "system", "content": system}, *messages]

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.xai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "store": False,
            },
        )
        response.raise_for_status()
        data = response.json()

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("xAI returned no choices")
    return choices[0]["message"]["content"].strip()


async def narrate_daily_reflection(payload: dict[str, Any]) -> str:
    name = payload.get("seeker_name", "Seeker")
    user_content = (
        f"Phoenix Oracle — daily conditions for {name}. "
        "Decode today's matrix from the JSON (numerology, bazi, vedic, western, natal_imprint_summary). "
        "Follow DAILY structure: address, today's field, steps, ritual. Blunt. No fluff.\n\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
    )
    return await chat_completion(
        system=DAILY_SYSTEM,
        user_content=user_content,
        model=settings.xai_model_daily,
        temperature=0.55,
    )


async def zero_reply(
    *,
    context: dict[str, Any],
    history: list[dict[str, str]] | None = None,
    user_message: str,
    memory_notes: list[str] | None = None,
) -> str:
    context_block = json.dumps(context, indent=2, ensure_ascii=False)
    memory_block = (
        "\n".join(f"- {n}" for n in memory_notes) if memory_notes else "(none)"
    )
    preamble = (
        "CHART CONTEXT (immutable + current hour — do not contradict):\n"
        f"{context_block}\n\nSEEKER MEMORY (themes they shared — use if present):\n"
        f"{memory_block}\n\nRespond to the seeker's latest message as Phoenix Forger Zero."
    )

    messages: list[dict[str, str]] = []
    if not history:
        messages.append({"role": "user", "content": preamble})
    else:
        messages.append({"role": "user", "content": preamble})
        for turn in history[-20:]:
            messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    return await chat_completion(
        system=ZERO_SYSTEM,
        messages=messages,
        model=settings.xai_model_zero,
        temperature=0.58,
    )


async def narrate_imprint_overview(payload: dict[str, Any]) -> str:
    max_words = payload.get("max_words", 1400)
    name = payload.get("seeker_name", "Seeker")
    user_content = (
        f"Master threshold seal for {name} (max {max_words} words). "
        "Match style_reference sections (vow, East:, West:, Cross:, optional Depth, Road, close). "
        f"Tighten — no repetition, no abstract filler. End {ZERO_SEAL_CLOSE}\n\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
    )
    return await chat_completion(
        system=OVERVIEW_SYSTEM,
        user_content=user_content,
        model=settings.xai_model_daily,
        temperature=0.65,
    )


async def narrate_location_insight(
    user_imprint: dict[str, Any],
    location_insight: dict[str, Any],
) -> str:
    from app.zero.context import imprint_summary

    name = user_imprint.get("birth", {}).get("display_name") or user_imprint.get("birth", {}).get("name") or "Seeker"
    payload = {
        "seeker_name": name,
        "natal_imprint_summary": imprint_summary(user_imprint),
        "location_insight": location_insight,
    }
    user_content = (
        f"Phoenix Oracle — location energy for {name}:\n\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
    )
    return await chat_completion(
        system=LOCATION_SYSTEM,
        user_content=user_content,
        model=settings.xai_model_zero,
        temperature=0.55,
    )