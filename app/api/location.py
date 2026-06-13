import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import assert_user_is_self, get_current_user, require_paid_tier
from app.models import User
from app.kb.loaders import load_states, state_by_code
from app.location.entity import build_entity_imprint
from app.location.insight import build_location_insight
from app.models import UserImprint
from app.schemas import LocationInsightRequest, LocationInsightResponse
from app.services.xai_client import narrate_location_insight

router = APIRouter(prefix="/location", tags=["location"])


async def _load_imprint(user_id: str, db: AsyncSession) -> dict:
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    return json.loads(row.imprint_json)


@router.get("/states")
async def list_states():
    return load_states()


@router.get("/states/{code}")
async def get_state_entity(code: str):
    rec = state_by_code(code)
    if not rec:
        raise HTTPException(status_code=404, detail="State not found")
    return {"record": rec, "entity_imprint": build_entity_imprint(rec)}


@router.post("/insight", response_model=LocationInsightResponse)
async def location_insight(
    body: LocationInsightRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assert_user_is_self(body.user_id, current_user)
    await require_paid_tier(body.user_id, db)
    imprint = await _load_imprint(body.user_id, db)
    insight = build_location_insight(
        imprint,
        state_code=body.state_code,
        city_name=body.city_name,
        latitude=body.latitude,
        longitude=body.longitude,
        include_companies=body.include_companies,
        vehicle=body.vehicle.model_dump() if body.vehicle else None,
    )
    narrative = None
    model = None
    if body.include_narration:
        if not settings.xai_api_key:
            narrative = "Set XAI_API_KEY for AI narration of location insight."
        else:
            try:
                narrative = await narrate_location_insight(imprint, insight)
                model = settings.xai_model_zero
            except Exception as exc:
                narrative = f"Narration failed: {exc}"

    return LocationInsightResponse(
        user_id=body.user_id,
        insight=insight,
        narrative=narrative,
        model=model,
    )


