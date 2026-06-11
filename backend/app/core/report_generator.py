from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import EloRating, Battle, WeaknessAnalysis, Report
from datetime import datetime


async def generate_model_report(model_id: int, task_ids: list[int], db: AsyncSession) -> dict:
    elo_result = await db.execute(
        select(EloRating).where(EloRating.model_id == model_id)
    )
    elo_rows = elo_result.scalars().all()
    elo_by_dimension = {
        r.dimension: {"rating": r.rating, "wins": r.wins, "losses": r.losses, "ties": r.ties}
        for r in elo_rows
    }

    battles_as_attacker = await db.execute(
        select(Battle).where(Battle.attacker_id == model_id)
    )
    battles_as_defender = await db.execute(
        select(Battle).where(Battle.defender_id == model_id)
    )
    attacker_battles = battles_as_attacker.scalars().all()
    defender_battles = battles_as_defender.scalars().all()

    attacker_wins = sum(1 for b in attacker_battles if b.winner == "attacker")
    defender_wins = sum(1 for b in defender_battles if b.winner == "defender")
    total = len(attacker_battles) + len(defender_battles)

    weakness_result = await db.execute(
        select(WeaknessAnalysis).where(WeaknessAnalysis.model_id == model_id)
    )
    weaknesses = [
        {"category": w.category, "fail_rate": w.fail_rate}
        for w in weakness_result.scalars().all()
    ]

    return {
        "model_id": model_id,
        "elo_by_dimension": elo_by_dimension,
        "overall_wins": attacker_wins + defender_wins,
        "total_battles": total,
        "win_rate": (attacker_wins + defender_wins) / total if total > 0 else 0.0,
        "weaknesses": weaknesses,
        "generated_at": datetime.utcnow().isoformat(),
    }


async def save_report(model_id: int, task_ids: list[int], report_type: str, db: AsyncSession) -> Report:
    content = await generate_model_report(model_id, task_ids, db)
    report = Report(
        model_id=model_id,
        task_ids=task_ids,
        report_type=report_type,
        content=content,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report
