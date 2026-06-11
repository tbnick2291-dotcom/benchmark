from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.adversarial_engine import AdversarialEngine
from app.core.elo import batch_update
from app.db.models import (
    EvaluationTask, Model, Battle, Question, EloRating, WeaknessAnalysis
)
from app.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def _get_or_create_elo(db: AsyncSession, model_id: int, dimension: str) -> EloRating:
    result = await db.execute(
        select(EloRating).where(EloRating.model_id == model_id, EloRating.dimension == dimension)
    )
    elo = result.scalar_one_or_none()
    if elo is None:
        elo = EloRating(model_id=model_id, dimension=dimension, rating=settings.elo_initial_rating)
        db.add(elo)
        await db.flush()
    return elo


async def _get_defender_weaknesses(db: AsyncSession, model_id: int, category: str | None) -> list[str]:
    result = await db.execute(
        select(WeaknessAnalysis).where(WeaknessAnalysis.model_id == model_id)
    )
    weaknesses = result.scalars().all()
    return [w.category for w in weaknesses if w.category]


async def run_benchmark_task(task_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(EvaluationTask).where(EvaluationTask.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        logger.error(f"Task {task_id} not found")
        return

    task.status = "running"
    await db.commit()

    config = task.config or {}
    model_ids: list[int] = config.get("model_ids", [])
    rounds: int = config.get("rounds", 5)
    dimension: str = task.dimension

    result = await db.execute(select(Model).where(Model.id.in_(model_ids)))
    models = result.scalars().all()
    if len(models) < 2:
        task.status = "failed"
        await db.commit()
        return

    engine = AdversarialEngine()

    for round_num in range(rounds):
        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                attacker = models[i]
                defender = models[j]
                defender_weaknesses = await _get_defender_weaknesses(db, defender.id, dimension)

                battle_result = await engine.run_battle(
                    attacker_model=attacker.model_path,
                    defender_model=defender.model_path,
                    dimension=dimension,
                    defender_weaknesses=defender_weaknesses,
                )

                question = Question(
                    task_id=task_id,
                    content=battle_result.question,
                    category=dimension,
                    generation_type="adversarial",
                    attacker_id=attacker.id,
                )
                db.add(question)
                await db.flush()

                battle = Battle(
                    question_id=question.id,
                    attacker_id=attacker.id,
                    defender_id=defender.id,
                    attacker_answer=battle_result.attacker_answer,
                    defender_answer=battle_result.defender_answer,
                    winner=battle_result.winner,
                    judge_reason=battle_result.judge_reason,
                    judged_by=attacker.id,
                )
                db.add(battle)

                attacker_elo = await _get_or_create_elo(db, attacker.id, dimension)
                defender_elo = await _get_or_create_elo(db, defender.id, dimension)

                if battle_result.winner == "attacker":
                    new_attacker, new_defender = batch_update(attacker_elo.rating, defender_elo.rating, settings.elo_k_factor)
                    attacker_elo.wins += 1
                    defender_elo.losses += 1
                elif battle_result.winner == "defender":
                    new_defender, new_attacker = batch_update(defender_elo.rating, attacker_elo.rating, settings.elo_k_factor)
                    defender_elo.wins += 1
                    attacker_elo.losses += 1
                else:
                    new_attacker = attacker_elo.rating
                    new_defender = defender_elo.rating
                    attacker_elo.ties += 1
                    defender_elo.ties += 1

                attacker_elo.rating = new_attacker
                defender_elo.rating = new_defender
                await db.commit()
                logger.info(f"Round {round_num}: {attacker.name} vs {defender.name} → {battle_result.winner}")

    task.status = "completed"
    task.completed_at = datetime.utcnow()
    await db.commit()
