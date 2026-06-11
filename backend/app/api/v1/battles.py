from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.db.models import Battle
from app.schemas.battles import BattleResponse

router = APIRouter(prefix="/battles", tags=["battles"])


@router.get("", response_model=list[BattleResponse])
async def list_battles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Battle).order_by(Battle.battle_time.desc()).limit(100))
    return result.scalars().all()


@router.get("/{battle_id}", response_model=BattleResponse)
async def get_battle(battle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Battle).where(Battle.id == battle_id))
    battle = result.scalar_one_or_none()
    if battle is None:
        raise HTTPException(status_code=404, detail="Battle not found")
    return battle
