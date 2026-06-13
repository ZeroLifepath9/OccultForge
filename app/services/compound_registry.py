"""
Full compound directory — every birth-date life-path compound (4–46) by final gate.
Each entry: occult glyph, equation, lookup citations, flesh, kin tag (siblings at same final).
"""

from __future__ import annotations

from typing import Any

# fmt: off — registry is data-dense
def _e(
    c: int,
    final: int,
    glyph: str,
    equation: str,
    citations: list[str],
    flesh: str,
    kin_tag: str,
) -> dict[str, Any]:
    return {
        "final": final,
        "glyph": glyph,
        "equation": equation,
        "citations": citations,
        "flesh": flesh,
        "kin_tag": kin_tag,
    }


# ── Final 1 — Monad Blade ─────────────────────────────────────────────────────
_D1 = {
    10: _e(10, 1, "the Crown Before the Throne", "1 + 0 → 1",
        ["Pythagorean 10: Wheel of Fortune — fate spins reputation before will is earned (look up: 10/1 numerology).",
         "Kabbalah: Keter touching Malkuth early — crown seen before root (Tree of Life, lightning flash).",
         "Tarot X → I: Wheel then Magician — become operator, not poster."],
        "You promote before you are ready; the room discovers the gap and the wheel turns against you.",
        "spin and visibility before inner 1"),
    19: _e(19, 1, "the Sun Prince", "1 + 9 → 10 → 1",
        ["19 = sun digit + ennead — leadership through completion of ego (look up: 19/1 'solar leader').",
         "Tarot: Sun (XIX) — visibility, vitality; reduce to Magician (I).",
         "Chaldean: 1 fire tested by 9's release — fame must survive an ending."],
        "You expect the spotlight to certify you; burnout when applause replaces skill.",
        "solar entitlement more than Wheel spin"),
    28: _e(28, 1, "the Veiled Crown", "2 + 8 → 10 → 1",
        ["2 = High Priestess; 8 = Strength/justice in matter — partnership before throne (Tarot II + VIII).",
         "28/1: power through alliance then solo claim (look up: 28 numerology leadership).",
         "Not 19/1: less solo sun, more contract-first kingship."],
        "You try to lead alone while secretly needing a consigliere — splits your authority.",
        "partnership veil before crown"),
    37: _e(37, 1, "the Analyst Crown", "3 + 7 → 10 → 1",
        ["3 = Empress/voice; 7 = Chariot of mysteries — speech + research → Wheel → 1.",
         "Look up: 37/1 'communicator king', Pythagorean 37 prime mystique.",
         "Tarot III + VII: teach, then command."],
        "You lead through ideas and analysis; paralysis when data replaces decision.",
        "mind and message before throne"),
    46: _e(46, 1, "the Mason Crown", "4 + 6 → 10 → 1",
        ["4 = Emperor/square; 6 = Lovers/hearth — structure + duty → public wheel → 1.",
         "Look up: 46/1 builder-leader, family business kings.",
         "Chaldean undertone: matter and beauty must agree before you stand first."],
        "You build institutions then claim the chair — resentment if you skip the foundation year.",
        "builder's law before solo blade"),
}

# ── Final 2 — Sacred Pair ─────────────────────────────────────────────────────
_D2 = {
    20: _e(20, 2, "the Judgment Pair", "2 + 0 → 2",
        ["20 = Judgment (Tarot XX) in the flesh — partnerships as courtroom (look up: 20/2 numerology).",
         "2 = High Priestess — mirror, patience, polarity.",
         "Angel 20: renewal through right alliance (study sacred scribes 20)."],
        "Every major bond feels fated and judged; you delay decisions until the room splits.",
        "only common 2-compound in births — judgment in union"),
}

# ── Final 3 — Living Word ─────────────────────────────────────────────────────
_D3 = {
    12: _e(12, 3, "the Offering", "1 + 2 → 3",
        ["12 = Hanged Man (Tarot XII) before Empress (III) — sacrifice teaches voice.",
         "Look up: 12/3 'apostle frequency', creative ordeal numerology.",
         "1 + 2: self yields to dyad before triad speaks."],
        "You create only after a cost — art born from what you gave up.",
        "ordeal before expression"),
    21: _e(21, 3, "the Crown of Voice", "2 + 1 → 3",
        ["21 = World (Tarot XXI) shrunk to triad — completion through speech (look up: 21/3).",
         "2 + 1: union then initiative → word.",
         "Not 30/3: less scatter, more dyad-crafted message."],
        "Your words marry two worlds; scandal when you speak for both sides at once.",
        "union-voice, not triple scatter"),
    30: _e(30, 3, "the Triple Voice", "3 + 0 → 3",
        ["30 = triad doubled in public — fame through expression (look up: 30/3 numerology).",
         "Tarot III Empress amplified — creation, fertility, performance.",
         "Risk: voice without root — study 30/3 scatter traps."],
        "Many platforms, many faces; exhaustion when none get your real story.",
        "public triad, not 12's sacrifice"),
    39: _e(39, 3, "the Hidden Triad", "3 + 9 → 12 → 3",
        ["3 + 9: creation meets completion — private art before public (look up: 39/3).",
         "12 undertone: offering — message after surrender.",
         "Not 21/3: more ennead weight, endings fund the craft."],
        "You finish chapters in private then publish; rage when someone previews the draft.",
        "completion-hidden before voice"),
}

# ── Final 4 — Stone Code ──────────────────────────────────────────────────────
_D4 = {
    4: _e(4, 4, "the Stone Code", "4 (single gate)",
        ["Tarot IV Emperor — square, law, foundation (look up: life path 4 builder).",
         "Pythagorean tetrad — four directions, four elements anchored.",
         "No compound split: flesh and vow are the same stone."],
        "What you build is who you are; shortcuts echo for years.",
        "one gate — no sibling compound at 4"),
    13: _e(13, 4, "the Phoenix Tax", "1 + 3 → 4",
        ["Tarot XIII Death → IV Emperor — transform then build (Thoth/Waite Death).",
         "13 karmic reinvention schools — systems break for identity (look up: 13/4).",
         "Chaldean: 4 waits beneath the burn."],
        "Every few years a false self must die — job, name, body image.",
        "fire before stone, not raw 4"),
    31: _e(31, 4, "the Veiled Builder", "3 + 1 → 4",
        ["3 + 1: voice + monad → law — teach then structure (look up: 31/4).",
         "31 prime — eccentric builder, independent craft.",
         "Not 13/4: less death, more message hardened into rules."],
        "You codify what you once performed — rigidity when the audience moves on.",
        "voice into stone"),
    40: _e(40, 4, "the Public Square", "4 + 0 → 4",
        ["40 = matter quadrupled in public — institution before soul (look up: 40/4).",
         "Emperor in the marketplace — reputation is architecture.",
         "4 + 0: structure seen before felt."],
        "You look established before you feel ready; maintain the facade or crack visibly.",
        "public stone, not phoenix burn"),
}

# ── Final 5 — Open Road ───────────────────────────────────────────────────────
_D5 = {
    5: _e(5, 5, "the Open Road", "5 (single gate)",
        ["Tarot V Hierophant / pentad — change, breath, the body in motion (look up: life path 5).",
         "Pythagorean 5: human form, five senses — freedom as physiology.",
         "Single gate: no compound argument — you are the road."],
        "Cages and lies cost you fast; honesty is oxygen.",
        "one gate at 5"),
    14: _e(14, 5, "the Tempest Ledger", "1 + 4 → 5",
        ["14 = Temperance/Angel split schools — appetite + law → movement (look up: 14/5).",
         "1 + 4: initiative chained to structure then breaks free.",
         "Tarot XIV: alchemy — vices converted to travel."],
        "You move when bored; consequence ledger follows — debts from old freedoms.",
        "tempest, not pure road"),
    23: _e(23, 5, "the Adventurer's Cross", "2 + 3 → 5",
        ["2 + 3: union + voice → change — relationships launch journeys (look up: 23/5).",
         "Prime 23 — royal five in some mystic tables.",
         "Not 14/5: less ledger, more duet-driven motion."],
        "Partners pick your destinations; rebellion when the dyad feels like a cage.",
        "partnership launches motion"),
    32: _e(32, 5, "the Voice of Change", "3 + 2 → 5",
        ["3 + 2: expression + intuition → road (look up: 32/5 numerology).",
         "Empress + Priestess — speak the hidden, then move.",
         "Not 41/5: more art, less law-break."],
        "You talk your way into new lives; scatter when every story ships half-finished.",
        "voice opens the road"),
    41: _e(41, 5, "the Lawbreaker", "4 + 1 → 5",
        ["4 + 1: structure + monad → rupture — rules then breakout (look up: 41/5).",
         "Builder who must flee the site — empire in motion.",
         "Not 14/5: less temperance, more deliberate break."],
        "You master systems then leave them; bosses call you traitor, disciples call you free.",
        "structure then break"),
}

# ── Final 6 — Hearth Seal ─────────────────────────────────────────────────────
_D6 = {
    6: _e(6, 6, "the Hearth Seal", "6 (single gate)",
        ["Tarot VI Lovers — beauty, duty, hexad (look up: life path 6 healer).",
         "Pythagorean 6: harmony, Venusian service.",
         "Single gate: love and labor are one rope."],
        "You heal by organizing beauty; control disguised as care is your main trap.",
        "one gate at 6"),
    15: _e(15, 6, "the Devil's Magnet", "1 + 5 → 6",
        ["15 = Devil (Tarot XV) → Lovers — magnetism with shadow price (look up: 15/6).",
         "1 + 5: lead the road into hearth — charisma binds.",
         "Study: 15/6 charm, addiction to being needed."],
        "You attract intensity; bonds turn possessive when you confuse heat with home.",
        "magnetism before hearth"),
    24: _e(24, 6, "the Hearth Throne", "2 + 4 → 6",
        ["24 = dyad + square — partnership + structure → home crown (look up: 24/6).",
         "Tarot II + IV: union legislated in the domestic.",
         "Not 42/6: smaller scale, less public family law."],
        "Family and partner are your empire; collapse when domestic law is unspoken.",
        "union-hearth"),
    42: _e(42, 6, "the Family Law", "4 + 2 → 6",
        ["4 + 2: builder + mirror → duty — lineage as contract (look up: 42/6).",
         "42 = answer metaphor in modern mysticism — service as path.",
         "Not 15/6: less devil charm, more obligation."],
        "You carry clan expectations; resentment when beauty becomes invoice.",
        "lineage law into hearth"),
}

# ── Final 7 — Inner Sanctum ───────────────────────────────────────────────────
_D7 = {
    7: _e(7, 7, "the Inner Sanctum", "7 (single gate)",
        ["Tarot VII Chariot of mysteries; seven seals, seven chakras ladder (look up: life path 7).",
         "Pythagorean heptad — thinker, hermit, analyst.",
         "Single gate: depth is the product."],
        "Surface jobs drain you even when they pay; solitude feeds output.",
        "one gate at 7"),
    16: _e(16, 7, "the Lightning Seat", "1 + 6 → 7",
        ["16 = Tower (Tarot XVI) → Chariot — ego lightning then mystic drive (look up: 16/7).",
         "1 + 6: lead the hearth into cave — humility or fracture.",
         "Study: tower numerology spiritual ambition."],
        "Sudden falls teach you; you distrust comfort after the strike.",
        "tower before sanctum"),
    25: _e(25, 7, "the Partnership Mystic", "2 + 5 → 7",
        ["2 + 5: union + road → research — love sends you inward (look up: 25/7).",
         "Prime 25 — square of five, freedom disciplined.",
         "Not 34/7: more bond, less solo study."],
        "You study people to study God; betrayal when partners read your notes.",
        "dyad fuels the cave"),
    34: _e(34, 7, "the Scholar", "3 + 4 → 7",
        ["3 + 4: voice + law → analysis — teach the system (look up: 34/7).",
         "Empress + Emperor: craft codified.",
         "Not 43/7: more public teaching, less hermit mason."],
        "You publish insight; loneliness when students want performance not truth.",
        "scholar's stone"),
    43: _e(43, 7, "the Hermit Mason", "4 + 3 → 7",
        ["4 + 3: structure + voice → cave — build the library (look up: 43/7).",
         "Prime 43 — eccentric priest-scientist.",
         "Not 16/7: slower than tower, deeper than lightning."],
        "You fortify knowledge; paranoia when the fortress has no door.",
        "mason hermit"),
}

# ── Final 8 — Material Crown ──────────────────────────────────────────────────
_D8 = {
    8: _e(8, 8, "the Material Crown", "8 (single gate)",
        ["Tarot VIII Strength/Justice — power, matter, infinity loop (look up: life path 8).",
         "Pythagorean octad — executive force, karmic balance in wealth.",
         "Single gate: gold must keep spine."],
        "You run things; win-at-all-costs empties the throne.",
        "one gate at 8"),
    17: _e(17, 8, "the Star After Strip", "1 + 7 → 8",
        ["17 = Star (Tarot XVII) → Strength — hope after stripping (look up: 17/8).",
         "1 + 7: lead the mystic into market — spiritual ambition with invoice.",
         "Not 26/8: more solo star, less union power."],
        "You rebuild reputation from ashes; impatience when the sky delays payment.",
        "star then crown"),
    26: _e(26, 8, "the Union Power", "2 + 6 → 8",
        ["2 + 6: dyad + hearth → wealth — partnership as empire (look up: 26/8).",
         "Chaldean 8 undertone: matter through mirror.",
         "Not 35/8: more home, less creative crown."],
        "You rise with a partner or against them; money is couples therapy.",
        "union power"),
    35: _e(35, 8, "the Creator Crown", "3 + 5 → 8",
        ["3 + 5: voice + road → executive — sell the journey (look up: 35/8).",
         "Empress + Hierophant: brand at scale.",
         "Not 44/8: more motion, less double matter."],
        "You monetize charisma; scandal when the product behind the brand is thin.",
        "creator executive"),
    44: _e(44, 8, "the Double Matter", "4 + 4 → 8",
        ["4 + 4: square doubled — institution squared (look up: 44/8 master builder shadow).",
         "Some schools read 44 as master 8 voltage — study 44 numerology karmic power.",
         "Not 17/8: less star, more concrete empire."],
        "You stack structures; rigidity when the second tower has no window.",
        "double emperor"),
}

# ── Final 9 — Ennead Gate ─────────────────────────────────────────────────────
_D9 = {
    9: _e(9, 9, "the Ennead Gate", "9 (single gate)",
        ["Tarot IX Hermit — completion, ennead, gestation nine months (look up: life path 9).",
         "Pythagorean nine: return, release, humanitarian close.",
         "Single gate: endings are craft."],
        "You finish, teach, release; savior fatigue when you hoard grief.",
        "one gate at 9"),
    18: _e(18, 9, "the Lunar Crown", "1 + 8 → 9",
        ["18 = Moon (Tarot XVIII) → Hermit — private tide before wisdom (look up: 18/9).",
         "9×2 doubled completion through emotion.",
         "Not 27/9 Sceptre, not 36/9 Throne — you mourn in hidden rooms."],
        "Endings hit through mood, family, memory — grief others do not see.",
        "private lunar completion"),
    27: _e(27, 9, "the Sceptre", "2 + 7 → 9",
        ["27 = 3×3×3 cube of nine (look up: 27 numerology compassion).",
         "Tarot II + VII: Priestess + Chariot — Sceptre, priest-king of cycles.",
         "Angel 27 as 9×3 service voltage — not 18/9 tide, not 36/9 stage."],
        "Exhausted by others' unfinished stories — genius and resentment one hand.",
        "field service authority"),
    36: _e(36, 9, "the Throne of Nine", "3 + 6 → 9",
        ["36 = 9×4 — completion through structure and voice (look up: 36/9 throne).",
         "Tarot III + VI: Empress + Lovers — public crown of release.",
         "Not 27/9 labor, not 18/9 private mourning."],
        "You need visible legacy; private completion feels like failure.",
        "public throne of release"),
    45: _e(45, 9, "the Stone Release", "4 + 5 → 9",
        ["4 + 5: law + road → ennead — build then walk away (look up: 45/9).",
         "Structure must end for wisdom to count.",
         "Not 18/9 feeling, not 27/9 service — you demolish to liberate."],
        "You close by destroying outdated forms; shock when others worship the ruins.",
        "builder's ending"),
}

# ── Master 11 — Master Channel ────────────────────────────────────────────────
_D11 = {
    11: _e(11, 11, "the Live Wire", "master 11",
        ["Master 11 — illumination vs breakdown (look up: Hans Decoz 11, sacred scribes 11).",
         "Tarot XI Justice — double pillar, nervous system as antenna.",
         "Single master gate when compound equals 11."],
        "Voltage in the nerve; prophecy without product scorches.",
        "master gate at 11"),
    29: _e(29, 11, "the Delayed Voltage", "2 + 9 → 11",
        ["29 → 11 — master in disguise (look up: 29/11 sensitive channel).",
         "2 + 9: union teaches completion before gate opens.",
         "Not 38/11: more delay, less expression blast."],
        "Sensitivity is unpaid antenna until you price it; relationships train the wire.",
        "partnership before master"),
    38: _e(38, 11, "the Expression Channel", "3 + 8 → 11",
        ["3 + 8: voice + power → master — teach at voltage (look up: 38/11).",
         "Empress + Strength — charisma channel.",
         "Not 29/11: more public speech, less union trial."],
        "You speak in lightning; audiences addicted, body fried.",
        "voice master"),
    47: _e(47, 11, "the Stone Channel", "4 + 7 → 11",
        ["4 + 7: law + mystery → master voltage (look up: 47/11 numerology).",
         "Emperor + Chariot — structure initiates the inner gate.",
         "Not 29/11: less partnership trial, more builder-mystic."],
        "You ground lightning in rules — body breaks when mystic skips the foundation.",
        "builder opens master gate"),
}

# ── Master 22 & 33 ────────────────────────────────────────────────────────────
_D22 = {
    22: _e(22, 22, "the Unbuilt Cathedral", "master 22",
        ["Master 22 — master mason, cathedral in muscle before tools (look up: 22 numerology).",
         "Tarot XXII as 0+22 Fool+builder arc — scale before stamina.",
         "Study: ground 22 or body fails blueprint."],
        "Vision exceeds spine; team and brick must catch the sky.",
        "sole master 22 compound"),
}
_D33 = {
    33: _e(33, 33, "the Christic Labor", "master 33",
        ["Master 33 — teacher-healer, love as labor (look up: 33 master number).",
         "Tarot Empress doubled — creation as sacrifice, symbolic not doctrinal.",
         "All schools warn: savior fatigue — invoice boundaries."],
        "Love as work; collapse when compassion has no floor price.",
        "sole master 33 compound"),
}

# Rare/low birth sums but used in name math — include for completeness
_D_EXTRA = {
    1: _e(1, 1, "the Monad Blade", "1 (single gate)",
        ["Tarot I Magician — pure initiative (look up: life path 1).", "Pythagorean monad — source.", "Single gate."],
        "You were sent to stand first; waiting feels like death.", "pure monad"),
    2: _e(2, 2, "the Sacred Pair", "2 (single gate)",
        ["Tarot II High Priestess — mirror, patience (look up: life path 2).", "Dyad — polarity.", "Single gate."],
        "Partnership is infrastructure; solo rots the polish.", "pure dyad"),
    3: _e(3, 3, "the Living Word", "3 (single gate)",
        ["Tarot III Empress — voice, creation (look up: life path 3).", "Triad — expression.", "Single gate."],
        "Silence costs more than speech; fame without root fails.", "pure triad"),
}

# Merge all directories
COMPOUND_DIRECTORY: dict[int, dict[str, Any]] = {}
for _block in (_D_EXTRA, _D1, _D2, _D3, _D4, _D5, _D6, _D7, _D8, _D9, _D11, _D22, _D33):
    COMPOUND_DIRECTORY.update(_block)

# Life-path final gates — insight + citations for every final
PATH_FINAL_DIRECTORY: dict[int, dict[str, Any]] = {
    1: {
        "glyph": "the Monad Blade",
        "plain": "Lead, start, and name the direction — do not wait for permission.",
        "insight": "Triumph when you stand center without apology; trial when pride burns bridges.",
        "citations": ["Tarot I Magician", "Pythagorean monad", "Look up: life path 1 leadership initiation"],
        "integration": "Ship one decision only you can make — today, visible, irreversible.",
    },
    2: {
        "glyph": "the Sacred Pair",
        "plain": "Grow through partnership and patience — the room is your instrument.",
        "insight": "Triumph in chosen mirror; trial in codependency and delayed decisions.",
        "citations": ["Tarot II High Priestess", "Dyad / lunar receptivity", "Look up: life path 2 diplomacy"],
        "integration": "Name one boundary in your closest bond — kind, specific, today.",
    },
    3: {
        "glyph": "the Living Word",
        "plain": "Communicate, create, perform — words and images are your product.",
        "insight": "Triumph when art converts noise; trial when performance outruns truth.",
        "citations": ["Tarot III Empress", "Triad / Mercury voice", "Look up: life path 3 expression"],
        "integration": "Publish one true sentence — post, pitch, or prayer — unfinished allowed.",
    },
    4: {
        "glyph": "the Stone Code",
        "plain": "Build slow, repeat sacredly, own the foundation.",
        "insight": "Triumph in outlasting; trial in rigidity and resentment of chaos.",
        "citations": ["Tarot IV Emperor", "Tetrahedron / four directions", "Look up: life path 4 builder"],
        "integration": "Ship one brick you will repeat for a year — document, payment, habit.",
    },
    5: {
        "glyph": "the Open Road",
        "plain": "Need variety, travel, honest talk — cages and lies cost fast.",
        "insight": "Triumph after honest risk; trial in broken oaths and motion addiction.",
        "citations": ["Tarot V Hierophant / pentad motion", "Five senses anthropology", "Look up: life path 5 freedom"],
        "integration": "Tell one truth before you move — job, city, or conversation.",
    },
    6: {
        "glyph": "the Hearth Seal",
        "plain": "Heal and organize — beauty, home, and duty are one rope.",
        "insight": "Triumph when home becomes temple; trial when care becomes control.",
        "citations": ["Tarot VI Lovers", "Hexad / Venus service", "Look up: life path 6 healer"],
        "integration": "Fix one domestic or aesthetic system — schedule, not sermon.",
    },
    7: {
        "glyph": "the Inner Sanctum",
        "plain": "Depth, study, solitude that feeds public clarity.",
        "insight": "Triumph when initiation completes; trial in isolation and hoarded secrets.",
        "citations": ["Tarot VII Chariot mysteries", "Seven seals / chakras ladder", "Look up: life path 7 hermit"],
        "integration": "Block four hours alone with one research question — no inbox.",
    },
    8: {
        "glyph": "the Material Crown",
        "plain": "Run resources ethically — power must feed legacy, not ego.",
        "insight": "Triumph in just command; trial in gold without spine.",
        "citations": ["Tarot VIII Strength", "Octad / infinity", "Look up: life path 8 executive karma"],
        "integration": "Audit one account — money, time, or energy — cut what dishonors conscience.",
    },
    9: {
        "glyph": "the Ennead Gate",
        "plain": "Close cycles cleanly — the Ennead Gate, not a generic helper archetype.",
        "insight": "Triumph in precise release; trial when compound habit performs savior or hoards grief.",
        "citations": ["Tarot IX Hermit", "Ennead / nine months gestation", "Look up: life path 9 completion vs compound 18/27/36"],
        "integration": "Close one door publicly this season — letter, resignation, archive.",
    },
    11: {
        "glyph": "the Master Channel",
        "plain": "Sense patterns early — ground voltage or the nerve owns you.",
        "insight": "Triumph when intuition ships; trial in prophecy without product.",
        "citations": ["Master 11 schools", "Angel 11 illumination", "Look up: 11 master number grounding"],
        "integration": "One insight → one tangible deliverable this week — no floating download.",
    },
    22: {
        "glyph": "the Master Mason",
        "plain": "Think big, build in phases — body and team must catch the vision.",
        "insight": "Triumph in world-touching work; trial when scale exceeds spine.",
        "citations": ["Master 22 cathedral", "Look up: 22 builder master", "Study phased rollout numerology"],
        "integration": "Cut the blueprint to the next 90 days only — one foundation pour.",
    },
    33: {
        "glyph": "the Master Healer",
        "plain": "Teach through care — boundaries are not optional.",
        "insight": "Triumph in disciplined compassion; trial in martyrdom.",
        "citations": ["Master 33 teacher-healer", "Look up: 33 christic labor symbolic", "Study healer boundaries"],
        "integration": "Set one fee or limit on help — time, money, or access.",
    },
}

# Sibling contrast lines auto-built per final
KINS_BY_FINAL: dict[int, str] = {}


def _build_kins() -> None:
    by_final: dict[int, list[tuple[int, str, str]]] = {}
    for c, data in COMPOUND_DIRECTORY.items():
        f = data["final"]
        by_final.setdefault(f, []).append((c, data["glyph"], data["kin_tag"]))

    for f, siblings in by_final.items():
        if len(siblings) <= 1:
            KINS_BY_FINAL[f] = (
                f"At final {f}, your compound is the primary signature — walk the gate, not generic path-{f} copy."
            )
            continue
        parts = [
            f"{c}/{f} {g} ({tag})" for c, g, tag in sorted(siblings, key=lambda x: x[0])
        ]
        KINS_BY_FINAL[f] = (
            f"At final {f}, these compounds are not one life: " + "; ".join(parts) + ". Know which body you inhabit."
        )


_build_kins()

# Chart modulation — works for any user seal
ELEMENT_MODULATION: dict[str, str] = {
    "Wood": "Wood day: grow before harvest — teach, plan, expand; cut dead wood quarterly or the compound rots on the vine.",
    "Fire": "Fire day: visibility is currency — pitch and perform on rhythm; impatience bankrupts the vow.",
    "Earth": "Earth day: compound slow in matter — meals, money, shelter, standards; panic-spend breaks the seal.",
    "Metal": "Metal day: contracts and cuts — precision is priestwork; sloppy partners forfeit the field.",
    "Water": "Water day: timing and reserves — step back before big signs; absorb others only on schedule.",
}

SUN_MODULATION: dict[str, str] = {
    "Aries": "Aries Sun: initiate endings — do not wait for consensus on what is finished.",
    "Taurus": "Taurus Sun: release must be tangible — asset, body, habit — or it did not happen.",
    "Gemini": "Gemini Sun: name it in writing — spoken closure without document returns.",
    "Cancer": "Cancer Sun: mood is evidence — honor grief schedule or the compound performs family drama.",
    "Leo": "Leo Sun: public dignity in closure — ugly exits stain longer than they should.",
    "Virgo": "Virgo Sun: closure is a checklist — ship the detail, not the speech.",
    "Libra": "Libra Sun: fairness and beauty in every exit — undocumented ugly sticks in reputation.",
    "Scorpio": "Scorpio Sun: depth before broadcast — secret chapters must be named to one trusted witness.",
    "Sagittarius": "Sagittarius Sun: truth in the promise — freedom requires you finish the old oath first.",
    "Capricorn": "Capricorn Sun: institutional closure — titles, records, timelines — informal quits boomerang.",
    "Aquarius": "Aquarius Sun: network knows before you announce — align allies or gossip owns the story.",
    "Pisces": "Pisces Sun: spiritual hygiene after release — solitude, water, art — or absorption returns the ghost.",
}

BRANCH_MODULATION: dict[str, str] = {
    "Rat": "Rat day: strategic finish — timing beats force; half-closures invite the same ghost.",
    "Ox": "Ox day: slow physical completion — outlast, do not dramatize rescue.",
    "Tiger": "Tiger day: bold cut when done — mercy without clarity feeds chaos.",
    "Rabbit": "Rabbit day: gentle exits still need a line — softness is not ambiguity.",
    "Dragon": "Dragon day: visible chapter ends — private finish feels like failure to your body.",
    "Snake": "Snake day: plan the sting — strike once, cleanly, without rehearsal gossip.",
    "Horse": "Horse day: motion after release — travel or workload shift anchors the new cycle.",
    "Goat": "Goat day: aesthetic and domestic peace — ugly home endings poison the next field.",
    "Monkey": "Monkey day: wit can sabotage closure — fewer jokes when signing the exit.",
    "Rooster": "Rooster day: precision cut — half-measures invite repeat performance.",
    "Dog": "Dog day: loyalty audit — who stayed when the compound was tired reveals the roster.",
    "Pig": "Pig day: feast then fast — celebrate release, then enforce the new boundary.",
}

COMPOUND_ELEMENT_HINT: dict[int, dict[str, str]] = {
    27: {
        "Earth": "Sceptre here is compassion as craft — shelter, standards, meals — not air-rescue fantasy.",
        "Water": "Sceptre here absorbs unfinished stories — schedule drainage or mood owns the ledger.",
        "Fire": "Sceptre here needs timed visibility — martyr without stage becomes resentment theater.",
    },
    18: {
        "Water": "Lunar Crown amplifies with Water — mood endings; solitude after every public yes.",
    },
    36: {
        "Fire": "Throne needs an audience for release — private completion feels like failure.",
    },
}

# Export flat glyph map for occult_wave
COMPOUND_GLYPH_EXPORT: dict[int, str] = {c: d["glyph"] for c, d in COMPOUND_DIRECTORY.items()}