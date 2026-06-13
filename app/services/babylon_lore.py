"""Occult lore for Chaldean digits, sign numbers, nakshatra, Babylon voice."""

from __future__ import annotations

CHALDEAN_DIGIT: dict[int, str] = {
    1: "the point — singular fate, kingship contested, you are sent to stand first or be broken by those who do",
    2: "the pair — alliance as law; peace is engineered, betrayal is passivity dressed as kindness",
    3: "the triad — speech as magic; what you say becomes terrain, scandal is unpaid prophecy",
    4: "the square — stone upon stone; the gods demand repetition, shortcuts are taxed in bone",
    5: "the quintet — roads open only after truth; change is oxygen, cages make you cruel",
    6: "the hexad — hearth and beauty as one rope; you heal or you control with care",
    7: "the heptad — veil and research; knowledge bought with distance, crowds drain the inner room",
    8: "the octad — matter obeys when conscience leads; gold without spine devours its owner",
    9: "the ennead — endings are craft; what you release returns as authority, clinging rots",
    11: "master light — voltage in the nerve; prophecy before product, ungrounded fire",
    22: "master mason — blueprint in heaven, body must catch scale or break",
    33: "master mercy — love as labor; sacrifice without boundary becomes theft",
}

SIGN_NUMBER: dict[str, int] = {
    "Aries": 1,
    "Taurus": 2,
    "Gemini": 3,
    "Cancer": 4,
    "Leo": 5,
    "Virgo": 6,
    "Libra": 7,
    "Scorpio": 8,
    "Sagittarius": 9,
    "Capricorn": 10,
    "Aquarius": 11,
    "Pisces": 12,
}

SIGN_CHALDEAN_BRIDGE: dict[int, str] = {
    1: "solar fire of initiation — the name-number and the sign-number both demand a head that will not bow",
    2: "lunar-earth patience — value accrues slow; the tablet warns against rushing the soil",
    3: "twin air — doubled mind; name and sign both broker worlds",
    4: "cardinal water — belonging as fortress",
    5: "royal fire — radiance taxed as duty",
    6: "sacred earth — service as priestcraft",
    7: "scales in air — justice purchased with delay",
    8: "fixed water — power through depth and leverage",
    9: "pilgrim fire — belief must become product or exile follows",
    10: "cardinal earth — time is the god you must court",
    11: "fixed air — tribe of the future, odd contracts",
    12: "mutable water — dissolution as gift and drowning as price",
}

NAKSHATRA_SCRIPT: dict[str, str] = {
    "Ashwini": "the chariot of healing speed — you begin before others approve",
    "Bharani": "the bearer — birth and death in one mouth; reinvention is not optional",
    "Krittika": "the cutter — purification by fire; sharp truth as vocation",
    "Rohini": "the red one — fertility, appetite, wealth through what is cultivated",
    "Mrigashira": "the searching gaze — quest without rest; dissatisfaction as engine",
    "Ardra": "the storm — grief that clears; tears as weather pattern",
    "Punarvasu": "the return of light — second chances after ruin",
    "Pushya": "the nourisher — protection, teaching, food as sacred law",
    "Ashlesha": "the entwined — hypnotic intelligence; venom when coiled too long",
    "Magha": "the ancestral throne — legacy, pride, kingship of blood",
    "Purva Phalguni": "pleasure before ripeness — romance, art, leisure as fate",
    "Uttara Phalguni": "patronage and contract — marriage of power and service",
    "Hasta": "the hand — craft, skill, theft of time through mastery",
    "Chitra": "the bright — architecture, beauty, spectacle",
    "Swati": "independent wind — trade, movement, refusal of cages",
    "Vishakha": "two-branched victory — ambition forked; choose one altar",
    "Anuradha": "devotion after delay — friendship as infrastructure",
    "Jyeshta": "the elder — seniority, rivalry, protection of throne",
    "Mula": "uprooting — endings that fund beginnings; no neutral ground",
    "Purva Ashadha": "invincible declaration — belief before proof",
    "Uttara Ashadha": "victory after ordeal — public triumph earned late",
    "Shravana": "the listener — fame through counsel, sacred hearing",
    "Dhanishta": "wealth drum — rhythm, music, resources in motion",
    "Shatabhisha": "the healer of wounds — secrecy, research, isolation as medicine",
    "Purva Bhadrapada": "funeral fire before dawn — intensity, penance, spiritual hunger",
    "Uttara Bhadrapada": "depth without drowning — wisdom after surrender",
    "Revati": "the wealthy shepherd — completion, safe passage, mercy at the road's end",
}

DASHA_SEASON: dict[str, str] = {
    "Ketu": "strip the ornament — spiritual audit, loss that clarifies",
    "Venus": "beauty, treaty, purse — charm as policy",
    "Sun": "visibility and father-law — crown or glare",
    "Moon": "mother, mood, public feeling — tides govern policy",
    "Mars": "strike, war, surgery — courage or collateral",
    "Rahu": "hunger for the foreign — obsession, scandal, systems broken open",
    "Jupiter": "expansion, counsel, law — mercy when honest",
    "Saturn": "delay, bone, institution — mastery through time or rigidity",
    "Mercury": "trade, speech, calculation — wit as survival",
}