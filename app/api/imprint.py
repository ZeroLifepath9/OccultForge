import json
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.imprint import compute_imprint
from app.models import BirthProfile, User, UserImprint
from app.schemas import ImprintMeResponse, ImprintPreviewResponse, ImprintResponse, SealImprintRequest
from app.services.bazi_enrich import ensure_bazi_canonical
from app.services.geocode import geocode_place
from app.services.interpretations.chart_readings_bundle import build_all_chart_readings
from app.services.overview_store import delete_overview, get_or_build_overview

router = APIRouter(prefix="/imprint", tags=["imprint"])


def _imprint_response(row: UserImprint) -> ImprintResponse:
    imprint = ensure_bazi_canonical(json.loads(row.imprint_json))
    return ImprintResponse(
        id=row.id,
        user_id=row.user_id,
        schema_version=row.schema_version,
        computed_at=row.computed_at,
        birth_fingerprint=row.birth_fingerprint,
        imprint=imprint,
    )


async def _imprint_me_payload(
    row: UserImprint,
    db: AsyncSession,
    *,
    refresh_overview: bool = False,
) -> dict:
    imprint_data = ensure_bazi_canonical(json.loads(row.imprint_json))
    overview = await get_or_build_overview(
        user_id=row.user_id,
        imprint=imprint_data,
        db=db,
        force=refresh_overview,
    )
    base = _imprint_response(row).model_dump()
    base["overview"] = overview
    try:
        base["chart_readings"] = build_all_chart_readings(imprint_data)
    except Exception as exc:
        base["chart_readings"] = {}
        base["chart_readings_error"] = str(exc)[:240]
    return base


async def _geo_from_seal_request(body: SealImprintRequest) -> dict[str, Any]:
    if body.latitude is not None and body.longitude is not None and body.timezone:
        return {
            "latitude": body.latitude,
            "longitude": body.longitude,
            "timezone": body.timezone,
            "display_name": body.place_of_birth,
            "place": body.place_of_birth,
        }
    try:
        return await geocode_place(body.place_of_birth)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Geocoding failed: {exc}") from exc


def _compute_imprint_from_seal(body: SealImprintRequest, geo: dict[str, Any]) -> dict[str, Any]:
    alias = (body.commonly_known_as or "").strip()
    return compute_imprint(
        display_name=body.name,
        birth_datetime_local=body.birth_datetime_local,
        timezone=geo["timezone"],
        latitude=geo["latitude"],
        longitude=geo["longitude"],
        birth_place_label=geo.get("display_name", body.place_of_birth),
        commonly_known_as=alias or None,
        gender=body.gender,
    )


@router.post("/preview", response_model=ImprintPreviewResponse)
async def preview_imprint(body: SealImprintRequest) -> ImprintPreviewResponse:
    """Compute imprint without auth — preview before account seal."""
    geo = await _geo_from_seal_request(body)
    imprint_data = ensure_bazi_canonical(_compute_imprint_from_seal(body, geo))
    chart_readings: dict[str, Any] = {}
    try:
        chart_readings = build_all_chart_readings(imprint_data)
    except Exception as exc:
        chart_readings = {"error": str(exc)[:240]}
    return ImprintPreviewResponse(imprint=imprint_data, chart_readings=chart_readings)


@router.post("/seal", response_model=ImprintMeResponse)
async def seal_imprint(
    body: SealImprintRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImprintMeResponse:
    existing_user_imprint = await db.execute(
        select(UserImprint).where(UserImprint.user_id == current_user.id)
    )
    if existing_user_imprint.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="You already have a sealed imprint. Sign in to view your chart.",
        )

    geo = await _geo_from_seal_request(body)

    user_id = current_user.id
    alias = (body.commonly_known_as or "").strip()
    profile = BirthProfile(
        user_id=user_id,
        display_name=body.name,
        birth_datetime_local=body.birth_datetime_local,
        timezone=geo["timezone"],
        latitude=geo["latitude"],
        longitude=geo["longitude"],
        birth_place_label=geo.get("display_name", body.place_of_birth),
        gender=body.gender,
    )
    db.add(profile)
    await db.flush()

    imprint_data = _compute_imprint_from_seal(body, geo)

    row = UserImprint(
        user_id=user_id,
        birth_profile_id=profile.id,
        schema_version=imprint_data["schema_version"],
        birth_fingerprint=imprint_data["birth_fingerprint"],
        imprint_json=json.dumps(imprint_data, ensure_ascii=False),
        computed_at=datetime.utcnow(),
        sealed=True,
    )
    db.add(row)
    await db.commit()
    await delete_overview(user_id, db)

    return await _imprint_me_payload(row, db, refresh_overview=True)


@router.get("/chart-anchor/me")
async def get_my_chart_anchor(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Verifiable BaZi anchors — day master vs year zodiac, audit checks."""
    from app.services.imprint_labels import build_display_bundle

    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == current_user.id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    imprint = json.loads(row.imprint_json)
    facts = build_display_bundle(imprint)
    return {
        "chart_anchor": facts.get("chart_anchor"),
        "pillars_hanzi": {
            k: imprint["bazi"]["pillars"][k]["gan_zhi"]
            for k in ("year", "month", "day", "hour")
        },
        "birth_local": imprint["birth"].get("datetime_local"),
        "timezone": imprint["birth"].get("timezone"),
    }


@router.get("/overview/version")
async def overview_version():
    from app.services.deep_seal_reading import READING_ENGINE

    return {
        "content_version": settings.overview_content_version,
        "template_signature": settings.overview_template_signature,
        "reading_kind": "threshold_seal",
        "reading_engine": READING_ENGINE,
        "xai_configured": bool(settings.xai_api_key),
    }


@router.get("/ancients-wisdom/me")
async def get_ancients_wisdom_me(
    current_user: User = Depends(get_current_user),
):
    """Ancient's Wisdom — chartless Zero layer; premium unlocks full transmission."""
    from app.services.interpretations.ancients_wisdom_lens import build_ancients_wisdom_response

    premium = settings.paid_dev_unlock or current_user.subscription_tier == "seeker"
    return build_ancients_wisdom_response(premium=premium)


@router.get("/chart-reading/me")
async def get_my_chart_reading(
    system: str = Query(
        ...,
        description="numerology|bazi|vedic|hellenistic|financial|combination|wealth|relationships",
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.interpretations.chart_system_readings import VALID_SYSTEMS, build_system_reading

    if system not in VALID_SYSTEMS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid system. Choose one of: {', '.join(sorted(VALID_SYSTEMS))}",
        )
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == current_user.id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    from app.services.interpretations.chart_reading_verify import ChartReadingVerificationError

    imprint = ensure_bazi_canonical(json.loads(row.imprint_json))
    try:
        return build_system_reading(system, imprint)
    except ChartReadingVerificationError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Chart reading failed self-check ({system}): {'; '.join(exc.errors[:5])}",
        ) from exc


@router.get("/overview/me")
async def get_my_overview(
    refresh: bool = Query(False, description="Force regenerate overview"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == current_user.id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    imprint = json.loads(row.imprint_json)
    return await get_or_build_overview(
        user_id=current_user.id,
        imprint=imprint,
        db=db,
        force=refresh,
    )


@router.post("/overview/me/refresh")
async def refresh_my_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == current_user.id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    imprint = json.loads(row.imprint_json)
    return await get_or_build_overview(
        user_id=current_user.id,
        imprint=imprint,
        db=db,
        force=True,
    )


@router.get("/me", response_model=ImprintMeResponse)
async def get_my_imprint(
    refresh_overview: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImprintMeResponse:
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == current_user.id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    return await _imprint_me_payload(row, db, refresh_overview=refresh_overview)


@router.get("/{user_id}", response_model=ImprintResponse)
async def get_imprint(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ImprintResponse:
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this imprint")
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found")
    return _imprint_response(row)