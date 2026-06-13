"""One-sentence life-path mission + birth-day execution rhythm (no number recitation)."""

from __future__ import annotations

from app.services.compound_occult import get_compound_entry
from app.services.interpretations.numerology_lived_voice import CALLING_BY_FINAL, FINAL_MEANS_PLAIN, WALK_BY_FINAL

# Compound+final → single mission sentence (wealth + seal overlay).
MISSION_BY_PAIR: dict[tuple[int, int], str] = {
    (27, 9): (
        "Open only what you can close fairly — carrying someone else's unfinished chapter is not your lane."
    ),
    (18, 9): (
        "Close private cycles with witness, not rescue theater — grief needs room, not a fixer."
    ),
    (36, 9): (
        "Finish in public when it matters — private completion alone will feel like failure."
    ),
    (45, 9): (
        "Demolish outdated forms to release — worshipping ruins blocks the next build."
    ),
    (10, 1): "Lead before the room votes — name direction and stand first.",
    (12, 3): "Create only after you chose the harder honest path — art follows sacrifice.",
    (13, 4): "Rebuild in documented phases — same spine, new chapter, no shortcut tax.",
    (17, 8): "Rebuild trust from delivery logs — accounts before applause.",
    (19, 1): "Let craft certify skill — applause alone is a brittle crown.",
    (21, 3): "Speak for one department at a time — duets scatter the message.",
    (28, 1): "Earn the solo title in the books before you wear it in public.",
    (30, 3): "Ship one finished piece before you multiply channels.",
}

BIRTHDAY_EXECUTION: dict[int, str] = {
    1: "Monthly rhythm: name one direction and act before consensus — initiative is upkeep.",
    2: "Monthly rhythm: polish one partnership — patience and boundaries are the maintenance hour.",
    3: "Monthly rhythm: finish a draft before you perform it — creation needs a closed loop.",
    4: "Monthly rhythm: repeat one brick — document, invoice, or habit that compounds trust.",
    5: "Monthly rhythm: tell truth before motion — honest risk beats restless escape.",
    6: "Monthly rhythm: fix one domestic or aesthetic system — service without controlling the table.",
    7: "Monthly rhythm: block cave time with one research question — depth before counsel.",
    8: "Monthly rhythm: audit one ledger — money, time, or energy cut to conscience.",
    9: "Monthly rhythm: close one door cleanly — endings teach when they stay documented.",
    11: "Monthly rhythm: land one insight as deliverable — voltage must become product.",
    22: "Monthly rhythm: pour one foundation this quarter — scale in human phases.",
    33: "Monthly rhythm: set one limit on help — care with fees and office hours.",
}


def life_path_mission_sentence(compound: int, final: int) -> str:
    """Single mission statement — never recites compound/final digits."""
    pair = (compound, final)
    if pair in MISSION_BY_PAIR:
        return MISSION_BY_PAIR[pair]
    display = f"{compound}/{final}" if compound != final else str(final)
    entry = get_compound_entry(compound, final, display)
    if entry and entry.get("shadow"):
        shadow = entry["shadow"].strip().rstrip(".")
        title = entry.get("title", "").replace("the ", "").strip()
        if title:
            return f"Your path is {title} — {shadow}."
        return f"{shadow.capitalize()}."
    calling = CALLING_BY_FINAL.get(final)
    if calling:
        clause = calling[0].replace("You are called to ", "").replace("you are called to ", "")
        return clause.rstrip(".") + "."
    return FINAL_MEANS_PLAIN.get(final, "Walk your finish order before you scale the next lane.").rstrip(".") + "."


def birthday_execution_clause(birthday_final: int) -> str:
    """How they execute monthly — no digit recitation."""
    if birthday_final in BIRTHDAY_EXECUTION:
        return BIRTHDAY_EXECUTION[birthday_final]
    walk = WALK_BY_FINAL.get(birthday_final)
    if walk:
        return walk[0].rstrip(".") + "."
    return FINAL_MEANS_PLAIN.get(birthday_final, "Repeat the upkeep that keeps income honest.").rstrip(".") + "."