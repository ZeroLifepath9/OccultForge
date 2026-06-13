"""Deterministic hourly overlay — BaZi hour pillar emphasis."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from lunar_python import Solar

from app.overlay.clashes import branch_clashes
from app.overlay.daily import build_daily_reflection_payload


def _bazi_pillar_at(local_dt: datetime) -> dict[str, str]:
    solar = Solar.fromYmdHms(
        local_dt.year,
        local_dt.month,
        local_dt.day,
        local_dt.hour,
        local_dt.minute,
        local_dt.second,
    )
    ec = solar.getLunar().getEightChar()
    return {
        "stem": ec.getTimeGan(),
        "branch": ec.getTimeZhi(),
        "gan_zhi": f"{ec.getTimeGan()}{ec.getTimeZhi()}",
    }


def build_hourly_advice_payload(
    imprint: dict[str, Any],
    at: datetime | None = None,
) -> dict[str, Any]:
    birth = imprint["birth"]
    tz = ZoneInfo(birth["timezone"])
    local_now = at or datetime.now(tz)
    if local_now.tzinfo is None:
        local_now = local_now.replace(tzinfo=tz)
    else:
        local_now = local_now.astimezone(tz)

    pillars = imprint["bazi"]["pillars"]
    natal_day = pillars["day"]
    current_hour = _bazi_pillar_at(local_now)

    clash_factors: list[str] = []
    for key, pillar in pillars.items():
        clash_factors.extend(
            branch_clashes(pillar["branch"], current_hour["branch"])
        )
    clash_factors = list(dict.fromkeys(clash_factors))

    daily = build_daily_reflection_payload(imprint, local_now.date())

    payload = {
        "timestamp_local": local_now.isoformat(),
        "timezone": birth["timezone"],
        "bazi": {
            "natal_day_pillar": natal_day["gan_zhi"],
            "day_master": imprint["bazi"]["day_master"]["stem"],
            "current_hour_pillar": current_hour["gan_zhi"],
            "hour_clashes_with_natal": clash_factors,
            "emphasis": "day_pillar_vs_hour_branch",
        },
        "daily_overlay": daily,
        "vedic": daily.get("vedic"),
        "numerology": daily["numerology"],
        "scores": {
            "hour_favorability": 0.3 if clash_factors else 0.7,
            "day_favorability": daily["scores"]["favorability"],
        },
    }
    payload["payload_hash"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]
    return payload