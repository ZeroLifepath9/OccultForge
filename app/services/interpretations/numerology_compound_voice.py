"""Compound-specific plain voice — subtitle, definition, scale, slim insight."""

from __future__ import annotations

import re
from typing import Any

from app.services.compound_occult import _compound_chart_hooks, get_compound_entry
from app.services.interpretations.manifestation_voice import plain_flesh
from app.services.interpretations.numerology_number_insight import build_compound_insight_layer

_COMPOUND_SUBTITLE: dict[int, str] = {
    10: "10 numerology — visibility before throne",
    13: "13 numerology — the phoenix/reinvention",
    17: "17 numerology — hope after strip-down",
    18: "18 numerology — lunar completion",
    27: "27 numerology — compassion",
    28: "28 numerology — alliance before crown",
    30: "30 numerology — voice as fate",
    36: "36 numerology — public release",
}

_COMPOUND_DEFINITION: dict[int, str] = {
    27: (
        "Exhausted by unfinished stories others leave open — partners, clients, family, rooms "
        "where cycles stall and someone must close them fairly. "
        "Compassion here is labor: scheduled care, clear standards, and the work of ending things properly — "
        "not vague kindness. Genius is the burden: you read what others miss, then carry the weight "
        "until you document a clean exit."
    ),
    18: (
        "Endings arrive through mood, memory, and private tide before the public ever hears the story. "
        "Completion happens in hidden rooms first — grief is real work, not performance. "
        "Compassion is lunar labor: feeling on a schedule so it becomes wisdom, not flood."
    ),
    36: (
        "You need visible legacy — private closure alone will feel like failure to your nervous system. "
        "Compassion is public labor: release that others can witness and learn from. "
        "Genius is the burden of carrying a crown others expect you to wear before you have rested."
    ),
    30: (
        "Voice is fate — one finished story must land before many platforms open. "
        "Creative labor is the compound: draft, proof, then broadcast. "
        "Scatter is the trap when applause arrives before the middle is written."
    ),
    17: (
        "Hope after strip-down — reputation rebuilt from ashes, not hype. "
        "Compassion is proof-based labor: show the work before you ask for the raise. "
        "Genius is the burden of seeing the star while others still want the old costume."
    ),
    28: (
        "Partnership and contract before solo crown — alliance is the forge, not the shortcut. "
        "Wealth labor runs through shared proof before the public title expands. "
        "Resentment arrives when you claim alone what was built together."
    ),
    10: (
        "Visibility before the throne is earned — the room sees you before the title is real. "
        "Leadership labor: one visible decision only after private work is done. "
        "Genius is early sight; burden is performing the crown before the foundation sets."
    ),
    13: (
        "Every few years a false self must die — job title, public name, or the body image you outgrew. "
        "Reinvention here is labor: scheduled endings, not drama — burn the old chapter, then pour stone. "
        "Genius is the burden: you see what must break before anyone else is ready to let it go."
    ),
}

_COMPOUND_SCALE: dict[int, dict[str, str]] = {
    18: {
        "left_label": "Composure",
        "left_text": "You hold the public face while tide runs underneath — discipline keeps the crown level.",
        "right_label": "Tide",
        "right_text": "Mood and memory pull hard — grief wants schedule, not suppression.",
    },
    24: {
        "left_label": "Home",
        "left_text": "Family law, hearth, and private duty — what must be kept in order.",
        "right_label": "Crown",
        "right_text": "Public myth and reputation — what the world expects you to perform.",
    },
    36: {
        "left_label": "Private close",
        "left_text": "Release that happens in the body first — endings you feel before you show.",
        "right_label": "Public throne",
        "right_text": "Legacy others must witness — invisible completion feels like failure here.",
    },
}

_CONTRACT_CLOSE = "It is not an easy road — it is the contract."

_FINAL_CLOSING: dict[int, str] = {
    1: (
        "You read what must be decided before the room votes. That nerve is your gift. "
        "When others want permission before proof, skip waiting with them — name direction, "
        "ship one move, then let them catch up. "
        "The stand you take is forged in private first. That is your forge. "
        "You cannot lead from a decision you have not finished. "
        "When you step forward, let the move be clean and visible — or respect never arrives. "
        "In full alignment, followership comes because the work was real first. "
        "Schedule the decision, write what earned the stand, then release the need for consensus. "
        "What survives is proof of nerve. The work returns when the next stand is yours to take. "
        f"{_CONTRACT_CLOSE}"
    ),
    2: (
        "You read what the bond needs before peace is performative. That mirror is your gift. "
        "When others want harmony without honesty, hold your boundary — "
        "name it kindly, then hold the line. "
        "Partnership work is private before the room calms. That is your forge. "
        "You cannot harmonize what you have not faced. "
        "When you repair, let the boundary be specific and on record — or calm is codependency. "
        "In full alignment, peace becomes infrastructure others rely on. "
        "Schedule the conversation, write what the mirror showed you, then release perfect-union fantasy. "
        "What survives is honest partnership. The work returns when the next bond needs your polish. "
        f"{_CONTRACT_CLOSE}"
    ),
    3: (
        "You know what must be finished before the broadcast opens. That clarity is your gift. "
        "When others want performance before the draft is real, skip the noise — "
        "finish one piece, then speak. "
        "The real work lives in private first. That is your forge. "
        "You cannot perform a truth you have not written. "
        "When you publish, let proof lead the voice — finished work on record, or the message is hollow. "
        "In full alignment, the work outlives applause. "
        "Schedule the draft, write what is true before it goes live, then release the urge to perform early. "
        "What survives is finished expression. The work returns when the next story calls. "
        f"{_CONTRACT_CLOSE}"
    ),
    4: (
        "You see what must be built before hype declares victory. That patience is your gift. "
        "When others want speed over structure, stay out of the chaos — lay one brick, repeat it, "
        "let trust compound. "
        "The discipline lives in private routine. That is your forge. "
        "You cannot skip the foundation year. "
        "When you claim results, let the habit be documented — brick on record, or wealth is brittle. "
        "In full alignment, trust and resources compound. "
        "Schedule the routine, write what you repeated, then release shortcuts. "
        "What survives is sacred repetition. The work returns when the next foundation needs you. "
        f"{_CONTRACT_CLOSE}"
    ),
    5: (
        "You read when motion is honest and when it is escape. That honesty is your gift. "
        "When others want noise before truth, name the truth first — speak what is real, "
        "then move with a spine. "
        "Freedom is forged in private clarity first. That is your forge. "
        "You cannot move cleanly from a lie you have not named. "
        "When you go, let the truth be spoken first — word before road, or freedom breaks its promise. "
        "In full alignment, freedom keeps its word. "
        "Schedule the truth, write what you are leaving and why, then release. "
        "What survives is honest motion. The work returns when the next road opens. "
        f"{_CONTRACT_CLOSE}"
    ),
    6: (
        "You see what home needs before beauty becomes control. That care is your gift. "
        "When others want you to fix without being asked, skip the lecture — "
        "repair one system, schedule the work, then step back. "
        "Service is forged in private duty first. That is your forge. "
        "You cannot heal a room you have not ordered in yourself. "
        "When you help, let beauty serve people — schedule, not sermon — or care becomes control. "
        "In full alignment, service and grace share one rope. "
        "Schedule the repair, write what order cost you, then release martyrdom. "
        "What survives is hearth that holds. The work returns when home needs you again. "
        f"{_CONTRACT_CLOSE}"
    ),
    7: (
        "You sense what must be studied before counsel is worth selling. That depth is your gift. "
        "When others want answers before initiation finishes, wait to teach — "
        "finish the question in solitude, then offer clarity. "
        "The study happens in private first. That is your forge. "
        "You cannot sell insight you have not earned. "
        "When you counsel, let the work be finished — proof before podium, or wisdom is performance. "
        "In full alignment, insight returns as clarity others can use. "
        "Schedule the solitude, write what the cave taught you, then release the urge to announce early. "
        "What survives is earned counsel. The work returns when the next question finds you. "
        f"{_CONTRACT_CLOSE}"
    ),
    8: (
        "You read when power is ethical and when appetite wears a crown. That audit is your gift. "
        "When others want gold without spine, audit instead — run the accounts, "
        "cut what dishonors conscience, then command. "
        "Power is forged in private audit first. That is your forge. "
        "You cannot wear a crown the books won't support. "
        "When you lead, let conscience precede expansion — accounts on record, or legacy empties. "
        "In full alignment, resources feed what lasts. "
        "Schedule the audit, write what conscience demanded, then release win-at-all-costs hunger. "
        "What survives is ethical command. The work returns when the next throne needs a spine. "
        f"{_CONTRACT_CLOSE}"
    ),
    9: (
        "You read when a cycle is complete before the room agrees. That sight is your gift. "
        "When others resist closure, finish your part, document it, "
        "and remove yourself from the equation. "
        "The heavy labor is private first. That is your forge. "
        "You cannot release what you have not finished. "
        "When you close, let the record be clean — fair ending on record, or it did not happen. "
        "In full alignment, mercy has teeth: wisdom offered, not imposed. "
        "Schedule the close, write what you learned, then release. "
        "What survives is the teaching. The work returns when the next ending finds you. "
        f"{_CONTRACT_CLOSE}"
    ),
    11: (
        "You sense voltage before the room has language for it. That antenna is your gift. "
        "When others want prophecy without product, ground the nerve instead — "
        "ground one signal into matter this week, then speak. "
        "The voltage grounds in private work first. That is your forge. "
        "You cannot announce intuition you have not built. "
        "When you ship, let matter precede the mystic — tangible proof, or the wire scorches. "
        "In full alignment, invention builds because nerve serves work. "
        "Schedule the build, write what the signal became, then release performance mysticism. "
        "What survives is grounded voltage. The work returns when the next charge arrives. "
        f"{_CONTRACT_CLOSE}"
    ),
    22: (
        "You see the cathedral before the foundation exists. That vision is your gift. "
        "When others want scale before stamina, keep human pace — "
        "ninety days, one pour, then the next brick. "
        "Scale is forged in private phases first. That is your forge. "
        "You cannot build sky without human pace. "
        "When you expand, let the foundation match the blueprint — phased proof on record, or the body fails. "
        "In full alignment, world-touching work lands because the spine kept up. "
        "Schedule the phase, write what the pour held, then release fantasy pace. "
        "What survives is built scale. The work returns when the next span needs you. "
        f"{_CONTRACT_CLOSE}"
    ),
    33: (
        "You feel the pull to heal before boundaries exist. That care is your gift. "
        "When others want rescue without price, skip martyrdom — set a fee, a limit, a schedule, "
        "then help. "
        "Compassion is forged with a spine in private first. That is your forge. "
        "You cannot teach through exhaustion. "
        "When you serve, let the boundary be named — help with terms on record, or love collapses. "
        "In full alignment, ascent happens without savior fatigue. "
        "Schedule the care, write what the boundary protected, then release unpaid rescue. "
        "What survives is bounded mercy. The work returns when the next student finds you. "
        f"{_CONTRACT_CLOSE}"
    ),
}

_AVATAR_FULL: dict[int, str] = {
    10: (
        "The room sees you before the title is real — visibility before the throne is earned. "
        "Leadership here is one visible decision only after private work is done. "
        "The trap is performing the crown before the foundation sets. "
        f"{_FINAL_CLOSING[1]}"
    ),
    13: (
        "Every few years a false self must die — a job title, a public image, "
        "or a picture of yourself you have already outgrown. "
        "Reinvention here is scheduled labor, not drama: burn the old chapter, then pour stone. "
        "The trap is clinging to an identity the room still applauds. "
        "You see what must break before anyone else is ready. That sight is your gift. "
        "When others cling to the old version, skip fighting their denial — schedule your burn, "
        "do your work, and let the chapter end. "
        "Reinvention happens in private first. That is your forge. "
        "You cannot leave a half-dead identity in public. "
        "When you exit an old self, document what you learned and what you build next — "
        "or the reinvention did not happen. "
        "In full alignment, you demolish outdated forms and pour stone after. "
        "Schedule the close, write what survived the fire, then release. "
        "What remains is the structure. The work returns when the next false self is ready to die. "
        f"{_CONTRACT_CLOSE}"
    ),
    17: (
        "You rebuild from ashes — reputation after strip-down, not hype. "
        "Hope here is proof-based labor: show the work before you ask for the raise. "
        "The trap is marketing the star before the product earns it. "
        f"{_FINAL_CLOSING[8]}"
    ),
    18: (
        "You feel endings before the public hears about them — through mood, memory, and private tide. "
        "Grief here is real work, not performance. "
        "Compassion is feeling on a schedule so it becomes wisdom, not flood. "
        "You sense what is finished in hidden rooms before anyone names it. That sight is your gift. "
        "When others want you to perform closure before you have felt it, honor your tide, not their timeline — "
        "honor the tide, then speak. "
        "The heavy feeling you carry is private. That is your forge. "
        "You cannot announce an ending you have not lived through. "
        "When you are ready to close, let the release be honest and on record — or it did not count. "
        "In full alignment, mood becomes wisdom others can use. "
        "Schedule the grief, write what the tide taught you, then release. "
        "What survives is honest release. The work returns when the next private ending finds you. "
        f"{_CONTRACT_CLOSE}"
    ),
    27: (
        "You are worn down by unfinished stories others leave open — in partnerships, at work, "
        "with family, wherever a cycle stalls and no one closes it fairly. "
        "You expect fair closure. Compassion here is the work: scheduled care, clear standards, "
        "and ending things properly — not performance. "
        "You read what must finish before the room agrees. That sight is your gift. "
        "When others resist closure, finish your part, document it, "
        "and remove yourself from the equation. "
        "The heavy load you carry is private. That is your forge. "
        "You cannot leave anything half-done. "
        "When you exit, it must be clean and on record, or it did not happen. "
        "In full alignment, you bring cycles to a close — fair and clean. "
        "Your mercy has teeth: wisdom forged through lived experience and a heavy contract, "
        "not rescue theater. Schedule the close, write what you learned, then release. "
        "What survives is the teaching; the work returns when the next unfinished story finds you. "
        f"{_CONTRACT_CLOSE}"
    ),
    28: (
        "You try to lead alone while needing alliance first — partnership and contract before solo claim. "
        "Wealth and authority here run through shared proof before the public title expands. "
        "The trap is claiming alone what was built together. "
        f"{_FINAL_CLOSING[1]}"
    ),
    30: (
        "You scatter across platforms when one finished story has not landed yet — "
        "many faces, many channels, exhaustion when none carry your real story. "
        "Voice is fate here: draft, proof, then broadcast — not applause before the middle is written. "
        f"{_FINAL_CLOSING[3]}"
    ),
    36: (
        "Private closure alone will feel like failure to you — you need visible legacy. "
        "Others must witness the lesson for it to land. "
        "Compassion here is public labor: release people can learn from, not quiet amnesia. "
        "You read when a cycle is complete and ready to teach the room. That sight is your gift. "
        "When others want invisible endings, finish in private, "
        "then bring the legacy where it can be seen. "
        "The crown you carry is heavy and often private first. That is your forge. "
        "You cannot claim completion without a witness. "
        "When you close, document it publicly — dignity on record, or it did not happen. "
        "In full alignment, your mercy has teeth: you end with legacy others can learn from. "
        "Schedule the close, write what you learned, then release. "
        "What survives is the teaching on record. "
        "The work returns when the next chapter needs a public finish. "
        f"{_CONTRACT_CLOSE}"
    ),
}

_COMPOUND_OPENING: dict[int, str] = {
    1: (
        "You were sent to stand first — pure initiative, no committee required. "
        "Waiting feels like death here; the work is naming direction and shipping before permission arrives."
    ),
    2: (
        "Partnership is infrastructure for you — the mirror polishes what solo effort cannot. "
        "Peace here is built through chosen bond, not endless delay."
    ),
    3: (
        "Silence costs more than speech — voice and creation are your product. "
        "Fame without root fails; one true story must land before the room multiplies."
    ),
    4: (
        "You build slow and repeat sacredly — the foundation is the whole argument. "
        "Hype is the enemy; one brick this week is the same brick next year."
    ),
    5: (
        "You need variety, travel, and honest talk — cages and lies cost fast. "
        "Motion here must start with truth, not noise."
    ),
    6: (
        "You heal and organize — beauty, home, and duty are one rope. "
        "Care becomes control when you lecture instead of repair."
    ),
    7: (
        "Depth, study, and solitude feed your public clarity. "
        "Initiation must finish before counsel is worth selling."
    ),
    8: (
        "You run resources and legacy — power must feed what lasts, not ego. "
        "Gold without spine empties the throne."
    ),
    9: (
        "You finish, teach, and release — endings are craft, not mood. "
        "Savior fatigue arrives when you hoard grief that was never yours to carry."
    ),
    11: (
        "Voltage lives in your nerve — illumination or breakdown, no middle shelf. "
        "Prophecy without product scorches; intuition must ship into matter."
    ),
    22: (
        "Vision exceeds ordinary spine — cathedrals want phased brick, not fantasy pace. "
        "Scale here is built at human speed or the body fails the blueprint."
    ),
    33: (
        "Love is labor for you — teaching and healing with a spine, not savior theater. "
        "Compassion without a floor price collapses the whole ascent."
    ),
    19: (
        "You expect the spotlight to certify you — leadership through visible vitality, not skill alone. "
        "Fame here must survive an ending before it counts as real. "
        "The trap is applause replacing the work underneath."
    ),
    37: (
        "You lead through ideas and analysis — speech and research before the throne. "
        "The trap is data replacing decision. Command here comes after teaching, not instead of it."
    ),
    46: (
        "You build institutions then claim the chair — structure and duty must agree before you stand first. "
        "The trap is taking the crown before the foundation year is honored."
    ),
    20: (
        "Every major bond feels fated and judged — partnership as courtroom, renewal through right alliance. "
        "You delay decisions until the room splits. Peace here needs a verdict, not endless waiting."
    ),
    12: (
        "You create only after a cost — sacrifice teaches the voice before expression lands. "
        "Art here is born from what you gave up. The offering comes before the triad speaks."
    ),
    21: (
        "Your words marry two worlds — union and initiative become one message. "
        "The trap is speaking for both sides at once when the room wants a single truth."
    ),
    39: (
        "You finish chapters in private then publish — creation meets completion before the public sees the work. "
        "Rage arrives when someone previews the draft. The message funds itself through surrender first."
    ),
    31: (
        "You build with vision veiled — voice and structure before the square is public. "
        "The trap is performing the builder before the blueprint is real."
    ),
    40: (
        "You build in full public view — the square doubled, institution as performance. "
        "The trap is rigidity when the structure has no room to breathe."
    ),
    14: (
        "Change and structure collide — tempest ledger, motion with accountability. "
        "The trap is freedom without the books that prove it."
    ),
    23: (
        "Adventure crosses partnership and voice — union plus expression before the open road. "
        "The trap is motion that outruns the bond you promised."
    ),
    32: (
        "Voice meets change — expression and partnership fuel the road. "
        "The trap is performing freedom while avoiding the hard conversation."
    ),
    41: (
        "Law and initiative meet on the road — structure challenged by the need to move. "
        "The trap is breaking rules without naming why."
    ),
    15: (
        "Magnetism and hearth pull hard — beauty with appetite, charm that can control. "
        "Service here needs a spine behind the allure."
    ),
    24: (
        "Home and law share the throne — hearth and structure before public duty. "
        "The trap is performing family order while private rooms unravel."
    ),
    42: (
        "Family law runs deep — structure and partnership as one domestic system. "
        "The trap is controlling the hearth instead of repairing it."
    ),
    16: (
        "Sudden falls teach you — ego lightning then mystic drive, tower before sanctum. "
        "The trap is trusting comfort after the strike."
    ),
    25: (
        "You study people to study depth — union and road send you inward. "
        "Research here runs through bond, not around it."
    ),
    34: (
        "You publish insight — voice and law codified into teaching. "
        "Loneliness arrives when students want performance, not truth."
    ),
    43: (
        "You fortify knowledge — structure and voice build the library in the cave. "
        "Wisdom here must have an exit, not just walls."
    ),
    26: (
        "You rise with a partner or against them — union and hearth into wealth. "
        "Money here is couples therapy if the contract is dishonest."
    ),
    35: (
        "You monetize charisma — voice and road into executive scale. "
        "Scandal follows when the product behind the brand is thin."
    ),
    44: (
        "You stack structures — institution squared, concrete empire over star hope. "
        "Rigidity arrives when the second tower has no window."
    ),
    45: (
        "You close by demolishing outdated forms — law and road into release. "
        "Shock follows when others worship the ruins you cleared."
    ),
    29: (
        "Sensitivity runs as unpaid antenna — union teaches completion before the master gate opens. "
        "Relationships train the wire until you price the voltage."
    ),
    38: (
        "You speak in lightning — voice and power into master channel. "
        "Public speech here must ground before it scales, or the body fries."
    ),
    47: (
        "You ground lightning in rules — structure initiates the inner master gate. "
        "Builder-mystic here pours stone before voltage."
    ),
}

_AVATAR_BY_FINAL: dict[int, str] = {
    f: f"{_COMPOUND_OPENING[f]} {_FINAL_CLOSING[f]}"
    for f in _FINAL_CLOSING
    if f in _COMPOUND_OPENING
}


def _extract_subtitle_from_citations(citations: list[str], c: int) -> str | None:
    for cite in citations:
        m = re.search(r"look up:\s*([^).]+)", cite, re.I)
        if m:
            tag = m.group(1).strip()
            if tag:
                return tag.replace("  ", " ")
        m = re.search(rf"{c}\s+numerology\s+\w+", cite, re.I)
        if m:
            return m.group(0).strip()
    return None


def build_compound_subtitle(c: int, f: int, lib: dict[str, Any]) -> str:
    if c in _COMPOUND_SUBTITLE:
        return _COMPOUND_SUBTITLE[c]
    cites = lib.get("citations") or []
    extracted = _extract_subtitle_from_citations(cites, c)
    if extracted:
        return extracted
    kin = plain_flesh(lib.get("kin", "")).split("—")[0].strip()
    if kin and len(kin) < 48:
        return kin
    if c == f:
        return f"{c} numerology — single gate"
    return f"{c} numerology — walks before {f}"


def build_compound_definition_expanded(c: int, f: int, lib: dict[str, Any]) -> str:
    if c in _COMPOUND_DEFINITION:
        return _COMPOUND_DEFINITION[c]
    flesh = plain_flesh(lib.get("flesh", ""))
    kin = plain_flesh(lib.get("kin", ""))
    if c == f:
        return flesh or kin or f"One gate {c} — body and vow share the same finish order."
    lead = flesh.split(".")[0] if flesh else ""
    if lead and kin and kin.lower() not in lead.lower():
        return f"{lead}. {kin}"
    return lead or kin or f"Compound {c} earns the body before final {f} settles."


def build_compound_scale(c: int, f: int) -> dict[str, str] | None:
    if c in _COMPOUND_SCALE:
        return dict(_COMPOUND_SCALE[c])
    return None


def build_compound_slim_insight(facts: dict[str, Any], c: int, f: int, disp: str) -> str:
    lib = get_compound_entry(c, f, disp)
    parts: list[str] = []
    eq = lib.get("equation", "")
    if eq and c != f:
        parts.append(f"Birth math: {eq} — the body runs {c} habits before {f} settles.")
    hooks = _compound_chart_hooks(facts, c, lib["glyph"])
    if hooks:
        parts.append(plain_flesh(hooks[0]))
    if not parts:
        pace = _COMPOUND_DEFINITION.get(c, "")
        if pace:
            parts.append(pace.split(".")[0] + ".")
    text = " ".join(parts[:2])
    words = text.split()
    if len(words) > 42:
        text = " ".join(words[:42]) + "."
    return text


def _opening_from_registry(lib: dict[str, Any]) -> str:
    flesh = plain_flesh(lib.get("flesh", ""))
    if flesh:
        return flesh.split(".")[0].strip() + "."
    kin = plain_flesh(lib.get("kin", ""))
    if kin:
        return kin.split("—")[0].strip() + "."
    return "Your compound earns the body before the final gate settles."


def _compose_avatar(c: int, f: int, lib: dict[str, Any] | None = None) -> str:
    if c in _AVATAR_FULL:
        return _AVATAR_FULL[c]
    if c == f and f in _AVATAR_BY_FINAL:
        return _AVATAR_BY_FINAL[f]
    opening = _COMPOUND_OPENING.get(c)
    if opening and f in _FINAL_CLOSING:
        return f"{opening} {_FINAL_CLOSING[f]}"
    if lib is None:
        lib = get_compound_entry(c, f, f"{c}/{f}" if c != f else str(c))
    if f in _FINAL_CLOSING:
        return f"{_opening_from_registry(lib)} {_FINAL_CLOSING[f]}"
    return (
        f"{_opening_from_registry(lib)} "
        "Your forge is finish order — body earns before voice speaks. "
        "Schedule the work, write what you learned, then release. "
        f"{_CONTRACT_CLOSE}"
    )


def build_avatar_text(c: int, f: int, facts: dict[str, Any], lib: dict[str, Any] | None = None) -> str:
    if lib is None:
        lib = get_compound_entry(c, f, f"{c}/{f}" if c != f else str(c))
    base = _compose_avatar(c, f, lib)
    layer = build_compound_insight_layer(c, f, lib)
    if layer:
        base = f"{base.rstrip('.')}. {layer}"

    expr = facts.get("expression") or {}
    soul = facts.get("soul_urge") or {}
    if expr.get("value") and soul.get("value") and expr["value"] != soul["value"]:
        base = (
            f"{base.rstrip('.')}. "
            "Your public name and private hunger run different calendars — "
            "close privately before you sign the public ending."
        )
    return base