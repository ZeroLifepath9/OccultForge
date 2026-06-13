import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import assert_user_is_self, get_current_user
from app.models import User, UserImprint, ZeroConversation, ZeroMemory, ZeroMessage
from app.schemas import ZeroChatRequest, ZeroChatResponse, ZeroMemoryCreate, ZeroMemoryResponse
from app.services.xai_client import zero_reply
from app.zero.context import build_zero_context

router = APIRouter(prefix="/zero", tags=["zero"])


async def _load_imprint(user_id: str, db: AsyncSession) -> dict:
    result = await db.execute(
        select(UserImprint).where(UserImprint.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Imprint not found — seal your chart first")
    return json.loads(row.imprint_json)


@router.post("/chat", response_model=ZeroChatResponse)
async def zero_chat(
    body: ZeroChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assert_user_is_self(body.user_id, current_user)
    if not settings.xai_api_key:
        raise HTTPException(
            status_code=503,
            detail="XAI_API_KEY not configured. Add it to backend/.env",
        )

    imprint = await _load_imprint(body.user_id, db)
    context = build_zero_context(imprint)

    conv_id = body.conversation_id
    if conv_id:
        conv = await db.get(ZeroConversation, conv_id)
        if not conv or conv.user_id != body.user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = ZeroConversation(user_id=body.user_id)
        db.add(conv)
        await db.flush()
        conv_id = conv.id

    hist_result = await db.execute(
        select(ZeroMessage)
        .where(ZeroMessage.conversation_id == conv_id)
        .order_by(ZeroMessage.created_at)
    )
    history = [
        {"role": m.role, "content": m.content}
        for m in hist_result.scalars().all()
    ]

    mem_result = await db.execute(
        select(ZeroMemory)
        .where(ZeroMemory.user_id == body.user_id)
        .order_by(ZeroMemory.created_at.desc())
        .limit(10)
    )
    memory_notes = [m.note for m in mem_result.scalars().all()]

    try:
        reply = await zero_reply(
            context=context,
            history=history,
            user_message=body.message,
            memory_notes=memory_notes,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"xAI request failed: {exc}") from exc

    db.add(ZeroMessage(conversation_id=conv_id, role="user", content=body.message))
    db.add(ZeroMessage(conversation_id=conv_id, role="assistant", content=reply))

    conv = await db.get(ZeroConversation, conv_id)
    if conv:
        conv.updated_at = datetime.utcnow()

    await db.commit()

    return ZeroChatResponse(
        conversation_id=conv_id,
        reply=reply,
        model=settings.xai_model_zero,
        context_snapshot={
            "hour_pillar": context["current_hour_overlay"]["bazi"]["current_hour_pillar"],
            "clashes": context["current_hour_overlay"]["bazi"]["hour_clashes_with_natal"],
            "ritual_candidates": context["ritual_candidates"],
        },
    )


@router.get("/context/{user_id}")
async def zero_context_preview(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assert_user_is_self(user_id, current_user)
    imprint = await _load_imprint(user_id, db)
    return build_zero_context(imprint)


@router.get("/memory/{user_id}", response_model=list[ZeroMemoryResponse])
async def list_zero_memory(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assert_user_is_self(user_id, current_user)
    result = await db.execute(
        select(ZeroMemory)
        .where(ZeroMemory.user_id == user_id)
        .order_by(ZeroMemory.created_at.desc())
    )
    rows = result.scalars().all()
    return [
        ZeroMemoryResponse(id=r.id, user_id=r.user_id, note=r.note, created_at=r.created_at)
        for r in rows
    ]


@router.post("/memory", response_model=ZeroMemoryResponse)
async def add_zero_memory(
    body: ZeroMemoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assert_user_is_self(body.user_id, current_user)
    row = ZeroMemory(user_id=body.user_id, note=body.note.strip())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return ZeroMemoryResponse(
        id=row.id, user_id=row.user_id, note=row.note, created_at=row.created_at
    )