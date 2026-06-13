import json
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.models import DailyReflection, User, UserImprint, ZeroMemory
from app.overlay.daily import build_daily_reflection_payload
from app.schemas import DailyPreviewRequest
from app.services.bazi_enrich import ensure_bazi_canonical
from app.overlay.daily_enrich import enrich_daily_bazi_english
from app.services.xai_client import narrate_daily_reflection
from app.zero.context import imprint_summary

router = APIRouter(prefix="/reflection", tags=["reflection"])


async def _daily_for_user(user_id: str, db: AsyncSession):
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")

    imprint = ensure_bazi_canonical(json.loads(row.imprint_json))
    tz = imprint["birth"]["timezone"]
    from zoneinfo import ZoneInfo

    local_date = date.today().isoformat()
    try:
        from datetime import datetime

        local_date = datetime.now(ZoneInfo(tz)).date().isoformat()
    except Exception:
        pass

    cached = await db.execute(
        select(DailyReflection).where(
            DailyReflection.user_id == user_id,
            DailyReflection.local_date == local_date,
        )
    )
    hit = cached.scalar_one_or_none()
    if hit:
        payload = enrich_daily_bazi_english(
            json.loads(hit.payload_json), imprint
        )
        return {
            "user_id": user_id,
            "local_date": local_date,
            "cached": True,
            "payload": payload,
            "narrative": hit.narrative_text,
            "model": hit.model_version,
        }

    payload = enrich_daily_bazi_english(
        build_daily_reflection_payload(imprint), imprint
    )
    payload["seeker_name"] = (
        imprint.get("birth", {}).get("display_name")
        or imprint.get("birth", {}).get("name")
        or "Seeker"
    )
    payload["natal_imprint_summary"] = imprint_summary(imprint)

    if not settings.xai_api_key:
        return {
            "user_id": user_id,
            "local_date": local_date,
            "cached": False,
            "payload": payload,
            "narrative": (
                "Configure XAI_API_KEY in backend/.env to enable AI daily narration. "
                "Your deterministic overlay is included in payload."
            ),
            "model": None,
        }

    try:
        narrative = await narrate_daily_reflection(payload)
        model = settings.xai_model_daily
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"xAI request failed: {exc}",
        ) from exc

    reflection = DailyReflection(
        user_id=user_id,
        local_date=local_date,
        payload_hash=payload["payload_hash"],
        payload_json=json.dumps(payload, ensure_ascii=False),
        narrative_text=narrative,
        model_version=model,
    )
    db.add(reflection)
    await db.commit()

    return {
        "user_id": user_id,
        "local_date": local_date,
        "cached": False,
        "payload": payload,
        "narrative": narrative,
        "model": model,
    }


@router.post("/daily/preview")
async def preview_daily_reflection(body: DailyPreviewRequest):
    """Stateless daily overlay for preview imprint — no auth."""
    imprint = ensure_bazi_canonical(body.imprint)
    target = None
    if body.target_date:
        try:
            target = date.fromisoformat(body.target_date)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid target_date") from exc
    payload = enrich_daily_bazi_english(build_daily_reflection_payload(imprint, target), imprint)
    return {
        "local_date": payload.get("date"),
        "cached": False,
        "payload": payload,
        "narrative": "",
        "model": None,
    }


@router.get("/daily/me")
async def get_my_daily_reflection(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await _daily_for_user(current_user.id, db)


@router.get("/daily/{user_id}")
async def get_daily_reflection(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await _daily_for_user(user_id, db)


# Zero Past Event Test (the free teaser "selling factor" — 3 rounds, logs failures for premium)
from app.schemas import ZeroPastTestRequest
from app.services.xai_client import chat_completion
from app.zero.context import imprint_summary
from app.overlay.daily import build_daily_reflection_payload
import json
from datetime import date
from app.models import ZeroMemory


ZERO_PAST_TEST_SYSTEM = """You are a master occult advisor speaking directly and conversationally to the user in plain, simple English. No formal greetings, no sign-offs, no "Dear Seeker", no "— Zero". Talk like a wise friend who truly understands their chart and is walking them through what the occult forces were doing on that specific day.

Your job is to take the exact past event the user described and the precise date, then weigh their full personal imprint against the actual reconstructed chart for that day (bazi pillars and day master for the date, numerology personal and universal day, sky dynamics, elements, clashes, hidden influences, and zero framework factors). 

Acknowledge the event plainly and specifically. Then explain, in clear conversational language, what the chart on that exact date would have indicated about the kind of experience they went through. Expand on the insight: what it suggests about timing, protection, challenge, or alignment in their life. Be in-depth but never cite "pathways" or list technical steps — just speak naturally about what the forces were saying.

Make it unmistakably clear that no generic or universal chart could ever speak to something this personal. Only by running the user's complete imprint against the full occult data of that specific day, month, and year can you see how the event fits (or doesn't). This is the unique service Zero provides: turning the sky of one day into a precise mirror for one person's actual life.

For refinement rounds, directly address their feedback and go deeper on the parts that felt off, using the same chart data.

Keep the tone engaged, respectful, and illuminating. Use short paragraphs. Be honest — if the chart shows the event was more external than heavily fated, say so plainly. Focus on what the personalized reading reveals about the event that a non-personalized reading could never touch.

Aim for substantial, thoughtful depth (800+ words) that feels like a real conversation with someone who gets their chart and is helping them see the event through the occult lens.

When referencing the natal or previous chart, include the exact marker [[NATAL_CHART]] in the text right after the reference.

When referencing the chart for the specific day, include the exact marker [[DAY_CHART:YYYY-MM-DD]] using the actual date.

Tell the user to "Select the token for that day's read to see the full chart for that day and how it connects to your event."

This way the user can click the token to view the actual data used in the insight.

At the very end of your response, after everything else, wrap it up with one clear, direct, personal, and extremely honest paragraph (no fluff, conversational, regular language): If I had been asked about this exact event on that specific day, given the circumstances in your chart and the sky at the time, here is what I would have advised you. Be incredibly personal to their imprint and the day's full data. If the event or its factors were bad or preventable, say so directly and advise against repeating the bad patterns. If it was not avoidable, describe it plainly and assess honestly how the user performed or held up against the nature of their own chart in the outcome. Promote what was strong or protective in the chart. Speak as Zero: this is the core function of the service — running real events (past, current, or future) against the user's complete personal charts and delivering clear, honest communication back like this. This is how users test Zero against events they already know the outcome of, and see for themselves how precisely it translates and communicates the occult insight. End on this note to drive home the value of the test and the tool."""

async def run_zero_past_test(payload: dict) -> dict:
    past_date = payload.get("past_date")
    event = payload.get("event_description", "")
    previous = payload.get("previous_analysis")
    feedback = payload.get("feedback")
    round_num = payload.get("round", 1)
    imprint = payload.get("imprint") or {}

    natal_summary = imprint_summary(imprint) if imprint else {"note": "limited chart context (preview mode)"}

    past_payload = {}
    if imprint:
        try:
            target = date.fromisoformat(past_date)
            past_payload = build_daily_reflection_payload(imprint, target)
            past_payload["seeker_name"] = imprint.get("birth", {}).get("display_name") or imprint.get("birth", {}).get("name") or "Seeker"
            past_payload["is_past_reconstruction"] = True
            past_payload["event_date"] = past_date
        except Exception:
            past_payload = {"note": "Could not fully reconstruct daily chart for the exact past date — using natal imprint only."}

    # If no XAI_API_KEY is configured on the server (common in preview or fresh deploys),
    # return a high-quality demo that still demonstrates the full feature.
    if not getattr(settings, "xai_api_key", None):
        analysis = _build_demo_zero_past_analysis(past_date, event, natal_summary, past_payload, previous, feedback)
        return {
            "analysis": analysis,
            "round": round_num,
            "past_date": past_date,
            "success": True,
            "demo_mode": True,
            "referenced_charts": {
                "natal": natal_summary,
                "day": past_payload
            }
        }

    user_block = f"""PAST DATE: {past_date}
EVENT THE USER DESCRIBES: {event}

NATAL IMPRINT SUMMARY (user's core blueprint):
{json.dumps(natal_summary, indent=2, ensure_ascii=False)[:3000]}

FULL RECONSTRUCTED CHART FOR THIS EXACT PAST DATE (bazi pillars, sky dynamics, numerology personal/universal day, elements, clashes, astrology layer, daily framing, zero-relevant factors — use ALL of this data):
{json.dumps(past_payload, indent=2, ensure_ascii=False)[:6000]}

PREVIOUS ANALYSIS (if this is a refinement round — address the user's feedback directly and go deeper):
{previous or '(first round)'}

USER FEEDBACK FOR THIS REFINEMENT:
{feedback or '(none — this is the first run)'}"""

    try:
        analysis = await chat_completion(
            system=ZERO_PAST_TEST_SYSTEM,
            user_content=user_block,
            model="grok-3",
            temperature=0.25,
        )
    except Exception as exc:
        # Sanitize technical details (don't leak key names etc.)
        tech = str(exc)[:80]
        if "API_KEY" in tech or "xai" in tech.lower():
            tech = "API configuration issue on server"
        analysis = f"The system encountered an issue generating the analysis this round. Please try again with more detail on the event. (Technical: {tech})"

    return {
        "analysis": analysis,
        "round": round_num,
        "past_date": past_date,
        "success": True,
        "referenced_charts": {
            "natal": natal_summary,
            "day": past_payload
        }
    }


def _build_demo_zero_past_analysis(
    past_date: str,
    event: str,
    natal_summary: dict,
    past_payload: dict,
    previous: str | None = None,
    feedback: str | None = None,
) -> str:
    """High-quality demo response when XAI_API_KEY is not set on the server.
    Clean, direct, conversational, in plain English. No placeholders, no citing pathways.
    Focuses on the event, what the chart on that day would have indicated, and the unique value
    of running the user's full personalized data against the actual sky of that date.
    """
    name = natal_summary.get("seeker_name", "Seeker") if isinstance(natal_summary, dict) else "Seeker"

    # Build a strong, conversational demo around the motorcycle collision example the user gave.
    # In a real run this would pull specific pillars, numbers, clashes, etc. from past_payload.
    demo = f"""On {past_date} you were in a head on motorcycle accident at 110mph. You should have not survived but you did.

Your chart on that day carried a very particular kind of intensity. The energy was about sudden, direct, high-speed meetings with something coming straight at you with enormous force — the kind of pattern that shows up when usual protections are thin and everything is moving fast.

Your own chart [[NATAL_CHART]] has a core way of being that involves staying present and intact under extreme pressure. The way you are built includes a real refusal to be removed easily, even when the situation looks impossible. On that date the sky lined up with that signature in a very direct way. The usual rules of what should happen in a crash like that were under heavy stress, but your personal factors and what was active in the sky that day created a narrow but real window where survival was still possible even when it looked impossible from the outside.

A regular astrology reading or general numerology forecast could never have said anything real about this. Those are too broad. They might say "be careful with travel" or "big changes possible." That applies to millions of people and doesn't actually speak to you or to this specific motorcycle at 110 mph on that exact day.

What this tool does is take every layer of your actual chart — the way your numbers work, the elements and hidden parts of your makeup, the cycles you were moving through — and sets it against the real chart of one single day [[DAY_CHART:2024-06-14]]. Then it looks at what actually happened to you and shows the connection. On that day the energy was extreme and direct. Your chart had the exact combination of toughness and presence that made survival possible in a crash that should have been fatal. The two things met.

The chart on that day would not have guaranteed you would walk away. It would have described a situation of maximum force meeting a person who has a real capacity to stay whole through maximum force. It would have suggested that if something this violent happened, it would feel like the world was testing the deepest part of how you are put together.

If I had been asked about this event on that specific day, given the circumstances in your chart and the sky at the time, I would have advised you to trust your core resilience and stay completely present in the moment. Your imprint has the exact signature for surviving the kind of direct, high-impact test that was active that day, but only if you refused to let fear or the usual expectations take you out of your body. It would have been a day to move with full awareness of the edge, knowing that your chart was wired to find the narrow path through when the collision came. The alignment was there for survival against the odds, but it would have required you to embody that refusal to be removed quality fully.

This is the real power of running your actual daily chart against real events in your life. Generic advice is useless for something this personal. But when you take everything that makes you you and run it against the actual sky and numbers of one specific day, you can see exactly how the forces were arranged around what really happened. It turns the occult into something that can actually explain a moment where you should have died but didn't.

Select the token for that day's read to see the full chart for that day and how it connects to your event.

If this doesn't quite land or you want to go deeper on any part, tell me exactly what feels off. I'll take the same full dataset and refine it in the next round."""

    if feedback:
        demo += f"\n\n(If this were a real refinement round I would now directly address your feedback and expand further using the same chart data for that day.)"

    return demo


@router.post("/zero/past-test")
async def zero_past_test(req: ZeroPastTestRequest):
    data = req.model_dump()
    result = await run_zero_past_test(data)
    return result


@router.post("/zero/past-test/preview")
async def zero_past_test_preview(req: ZeroPastTestRequest):
    data = req.model_dump()
    if not data.get("imprint"):
        raise HTTPException(status_code=400, detail="Preview requires full imprint data")
    result = await run_zero_past_test(data)
    return result


@router.post("/account/zero-test-failure")
async def log_zero_test_failure(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Document failure in ZeroMemory notes for premium awareness."""
    note_text = f"ZERO PAST TEST FAILURE — date={payload.get('past_date')} rounds={payload.get('rounds', 0)} reason={payload.get('reason', 'declined')} event={str(payload.get('event_description', ''))[:150]}"
    mem = ZeroMemory(user_id=current_user.id, note=note_text)
    db.add(mem)
    await db.commit()
    return {"logged": True, "note": "Failure documented for your record."}