"""Delete user chart data or full account — allows re-seal and re-register."""

from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    BirthProfile,
    DailyReflection,
    NatalOverview,
    User,
    UserImprint,
    ZeroConversation,
    ZeroMemory,
    ZeroMessage,
)


async def delete_user_chart_data(user_id: str, db: AsyncSession) -> bool:
    """Remove imprint, profiles, overviews, daily cache — user row stays."""
    imprint = (
        await db.execute(select(UserImprint).where(UserImprint.user_id == user_id))
    ).scalar_one_or_none()
    if not imprint:
        return False

    await db.execute(delete(DailyReflection).where(DailyReflection.user_id == user_id))
    await db.execute(delete(NatalOverview).where(NatalOverview.user_id == user_id))
    await db.execute(delete(BirthProfile).where(BirthProfile.user_id == user_id))
    await db.delete(imprint)
    await db.commit()
    return True


async def delete_user_account(user_id: str, db: AsyncSession) -> bool:
    """Remove user and all related rows — email can register again."""
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return False

    conv_ids = [
        row[0]
        for row in (
            await db.execute(
                select(ZeroConversation.id).where(ZeroConversation.user_id == user_id)
            )
        ).all()
    ]
    if conv_ids:
        await db.execute(delete(ZeroMessage).where(ZeroMessage.conversation_id.in_(conv_ids)))
    await db.execute(delete(ZeroConversation).where(ZeroConversation.user_id == user_id))
    await db.execute(delete(ZeroMemory).where(ZeroMemory.user_id == user_id))
    await db.execute(delete(DailyReflection).where(DailyReflection.user_id == user_id))
    await db.execute(delete(NatalOverview).where(NatalOverview.user_id == user_id))
    await db.execute(delete(UserImprint).where(UserImprint.user_id == user_id))
    await db.execute(delete(BirthProfile).where(BirthProfile.user_id == user_id))
    await db.delete(user)
    await db.commit()
    return True