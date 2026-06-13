from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.services.account_reset import delete_user_account, delete_user_chart_data

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/reset-chart")
async def reset_chart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete sealed imprint so this account can enter a new birth chart."""
    removed = await delete_user_chart_data(current_user.id, db)
    if not removed:
        raise HTTPException(status_code=404, detail="No sealed chart to reset.")
    return {"ok": True, "message": "Chart cleared. You can enter a new birth story."}


@router.post("/delete")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete account and all data — same email can register again."""
    await delete_user_account(current_user.id, db)
    return {"ok": True, "message": "Account deleted. You can create a new one with this email."}


@router.post("/upgrade-dev")
async def upgrade_dev(user_id: str, db: AsyncSession = Depends(get_db)):
    if settings.is_production:
        raise HTTPException(status_code=404, detail="Not found")
    if not settings.paid_dev_unlock:
        raise HTTPException(status_code=403, detail="Dev upgrade disabled")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.subscription_tier = "seeker"
    await db.commit()
    return {"user_id": user_id, "subscription_tier": "seeker"}