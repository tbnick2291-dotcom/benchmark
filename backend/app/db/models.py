from datetime import datetime
from sqlalchemy import (
    Integer, String, Float, Text, ForeignKey, TIMESTAMP, ARRAY,
    func, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    model_path: Mapped[str] = mapped_column(String(500), nullable=False)
    config: Mapped[dict | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(20), default="inactive")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class EvaluationTask(Base):
    __tablename__ = "evaluation_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    dimension: Mapped[str] = mapped_column(String(50), nullable=False)
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)
    config: Mapped[dict | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("models.id"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("evaluation_tasks.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    difficulty: Mapped[str | None] = mapped_column(String(20))
    generation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    attacker_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("models.id"))
    expected_answer: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class Battle(Base):
    __tablename__ = "battles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("questions.id"))
    attacker_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("models.id"))
    defender_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("models.id"))
    attacker_answer: Mapped[str | None] = mapped_column(Text)
    defender_answer: Mapped[str | None] = mapped_column(Text)
    winner: Mapped[str | None] = mapped_column(String(20))
    judge_reason: Mapped[str | None] = mapped_column(Text)
    judged_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("models.id"))
    battle_time: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class EloRating(Base):
    __tablename__ = "elo_ratings"
    __table_args__ = (UniqueConstraint("model_id", "dimension"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("models.id"), nullable=False)
    dimension: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=1500.0)
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    ties: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class WeaknessAnalysis(Base):
    __tablename__ = "weakness_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("models.id"), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    fail_rate: Mapped[float | None] = mapped_column(Float)
    typical_errors: Mapped[dict | None] = mapped_column(JSONB)
    attack_patterns: Mapped[dict | None] = mapped_column(JSONB)
    last_updated: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("models.id"), nullable=False)
    task_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer))
    report_type: Mapped[str | None] = mapped_column(String(50))
    content: Mapped[dict | None] = mapped_column(JSONB)
    generated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
