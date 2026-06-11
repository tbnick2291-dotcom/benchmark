from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.db.models import Question
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/questions", tags=["questions"])


class QuestionResponse(BaseModel):
    id: int
    task_id: int | None
    content: str
    category: str | None
    difficulty: str | None
    generation_type: str
    attacker_id: int | None
    expected_answer: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
