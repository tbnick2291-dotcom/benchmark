from pydantic import BaseModel
from datetime import datetime


class BattleResponse(BaseModel):
    id: int
    question_id: int | None
    attacker_id: int | None
    defender_id: int | None
    attacker_answer: str | None
    defender_answer: str | None
    winner: str | None
    judge_reason: str | None
    judged_by: int | None
    battle_time: datetime

    model_config = {"from_attributes": True}
