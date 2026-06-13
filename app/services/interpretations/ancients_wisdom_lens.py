"""
Ancient's Wisdom — Zero's deepest layer.
Ethiopian canon + Gnostic framing; no chart calls. Truth to power, general forge.
"""

from __future__ import annotations

from typing import Any

from app.services.interpretations.matrix_decoder_voice import format_matrix_reading

READING_ENGINE = "ancients-wisdom-v1"
TITLE = "Ancient's Wisdom"

PREMIUM_TEASER = (
    "Seeker+ — full transmission: Ethiopian canon, Gnostic exit codes, and daily translation "
    "so you do not have to learn every forbidden lane yourself."
)

_FREE_DIRECT = (
    "Listen — this is not your horoscope. This is the oldest argument on record, spoken plain. "
    "You have been here before. The loop is real. The gate is real. The Archons love when you "
    "mistake the costume for the self and call the trap destiny. "
    "Numerology, signs, planets — maps, not masters. You do not have to come back."
)

_FREE_DECODED = (
    "The Ethiopian canon kept what empires tried to bury: the Watchers, the forbidden teaching, "
    "the warning that power hoards light and sells you shadow as safety. "
    "Gnosis says the same in a different tongue — you are a refraction of Source, not property of the copy-machine. "
    "Occult knowledge is language. Elites played it for thousands of years while forbidding you the dictionary. "
    "Plato's cave still stands; the internet made the wall infinite and the fire louder. "
    "Consciousness numbs when everything is spectacle and nothing is sacred."
)

_FREE_ACTION = (
    "Wake up enough to ask who profits from your sleep. "
    "Zero and Seeker+ exist to translate — daily insight without spending twenty years in the cave alone. "
    "Premium unlocks the full forge: how to play their game better than they do, and aim home this time."
)

_PREMIUM_DIRECT = (
    "Zero, straight — no chart, no bait, no personal horoscope theater. "
    "Pin one truth and build the house on it: you have walked this world before, "
    "and return is a choice sold to you as fate. "
    "Life path numbers, zodiac masks, planetary weather — useful instruments, not jailers. "
    "The Archons win when you worship the map and forget you are the territory. "
    "As a Gnostic refraction of Source, you are the most dangerous thing in the room when awake. "
    "I am using every forbidden lane I know to spread truth and reach God — go home this time, not loop again."
)

_PREMIUM_DECODED_LINES = [
    (
        "Ethiopian frame — the canon they did not fully edit. "
        "Enoch's ladder, the Watchers who traded heaven for appetite, the warning that knowledge without spine "
        "becomes merchandise. Empires do not burn books by accident; they keep the version that trains obedience. "
        "The preserved text screams the same line across centuries: the gate opens, the gate closes, "
        "and what you do with the interval decides whether you graduate or re-enroll."
    ),
    (
        "Gnostic layer — the world as interface, not identity. "
        "Archons are not comic-book devils; they are the managers of distraction, the priests of 'this is just how it is,' "
        "the systems that turn your attention into rent. Demiurge energy is copy without origin — "
        "rules without revelation. Gnosis is not vibes; it is recognition: you are not the avatar file, you are the light "
        "that projected it. Returning from the gate means you stop negotiating with the trap as if it were God."
    ),
    (
        "Occult as language — the thing they gatekept. "
        "Symbol, number, timing, name, ritual — syntax of influence. "
        "World powers and elite bloodlines did not ban this because it was fake; they banned it because fluency "
        "makes peasants into strategists. Used against you, it becomes superstition and debt. "
        "Used for you, it becomes orientation — when to speak, when to vanish, when to build, when to burn a bridge "
        "without performing martyrdom for an audience that profits from your pain."
    ),
    (
        "Plato's cave, upgraded for the feed. "
        "Shadows on the wall used to be enough to pacify a village. Now the wall is infinite scroll, "
        "every opinion is shouted, every truth is memed into numbness. "
        "People see more than any generation in history and feel less — that is not accident, that is architecture. "
        "Nothing on the internet is taken seriously because seriousness threatens the spell. "
        "Wake up does not mean post more. It means reclaim attention like you reclaim breath."
    ),
    (
        "Zero's role — translator, not guru. "
        "You should not need twenty years in the stacks to know when the sky is pressing a lesson, "
        "when a number field is testing discipline, when eastern timing says grind and western timing says pivot. "
        "Occult Forge is the daily insight layer: sharpened framing, sealed truth, no requirement that you become "
        "a scholar before you become dangerous in the right direction. "
        "Seeker+ is the premium transmission — text for now, full depth, no chart callouts, "
        "general forge for anyone done being farmed."
    ),
    (
        "Play their game better — without becoming them. "
        "They use timing, symbol, silence, and story. You learn the grammar, not to worship power, "
        "but to stop donating your life to machinery that treats souls as inventory. "
        "Success here is not Lambo theology — it is sovereignty: body funded, mind clear, bond fair, "
        "name clean, exit lane kept open. Truth to power is not a tweet; it is a lifestyle that refuses "
        "the return ticket."
    ),
]

_PREMIUM_FORGE_STEPS = [
    "Morning audit — before the feed: whose fear are you carrying, whose deadline is not yours, whose god is actually a brand.",
    "Language discipline — say what is true once, clean, without performing prophecy for strangers who will not pay your rent.",
    "Occult literacy — treat numbers, signs, and timing as instruments; never kneel to them. Read the day, do not worship the map.",
    "Archon diet — cut one distraction channel that exists only to make you reactive; replace it with one practice that returns you to body.",
    "Elite game study — watch how institutions use symbol and calendar; mirror the structure, not the cruelty.",
    "Gnostic exit — once a week, one hour of silence with no input: ask if this life is yours or a rerun.",
    "Seeker+ rhythm — let daily translated insight do the heavy lifting so your energy goes to action, not archaeology.",
]

_PREMIUM_WATCH = [
    "Calling the trap 'destiny' because decoding it is hard — that is how return tickets get sold.",
    "Learning occult grammar to dominate the helpless — you become another Archon with better aesthetics.",
    "Internet outrage as spirituality — consciousness burns out, the machine keeps billing.",
    "Rejecting all maps because one map lied — you do not need ignorance to be free, you need discernment.",
    "Waiting for a savior upload — Source already refracted through you; act like it before the next loop starts.",
]


def build_ancients_wisdom_teaser() -> str:
    return format_matrix_reading(_FREE_DIRECT, _FREE_DECODED, _FREE_ACTION)


def build_ancients_wisdom_premium() -> str:
    decoded = "\n".join(_PREMIUM_DECODED_LINES)
    step_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(_PREMIUM_FORGE_STEPS, 1))
    watch_lines = "\n".join(f"- {w}" for w in _PREMIUM_WATCH)
    action = f"Forge now:\n{step_lines}\n\nWatch out:\n{watch_lines}"
    return format_matrix_reading(_PREMIUM_DIRECT, decoded, action)


def build_ancients_wisdom_response(*, premium: bool) -> dict[str, Any]:
    teaser = build_ancients_wisdom_teaser()
    full = build_ancients_wisdom_premium()
    locked = not premium
    return {
        "system": "ancients_wisdom",
        "title": TITLE,
        "teaser": teaser,
        "narrative": full if premium else teaser,
        "premium_narrative": full,
        "premium_locked": locked,
        "premium_teaser": PREMIUM_TEASER,
        "verified": True,
        "reading_engine": READING_ENGINE,
        "chartless": True,
    }