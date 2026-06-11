from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.db.models import EloRating, Model
from app.schemas.leaderboard import EloEntry

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[EloEntry])
async def get_leaderboard(
    dimension: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(EloRating, Model.name).join(Model, EloRating.model_id == Model.id)
    if dimension:
        query = query.where(EloRating.dimension == dimension)
    query = query.order_by(EloRating.rating.desc())
    result = await db.execute(query)
    rows = result.all()
    return [
        EloEntry(
            model_id=elo.model_id,
            model_name=name,
            dimension=elo.dimension,
            rating=elo.rating,
            wins=elo.wins,
            losses=elo.losses,
            ties=elo.ties,
        )
        for elo, name in rows
    ]
