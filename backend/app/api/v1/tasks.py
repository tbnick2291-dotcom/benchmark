from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.db.models import EvaluationTask
from app.schemas.tasks import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EvaluationTask))
    return result.scalars().all()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = EvaluationTask(**payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EvaluationTask).where(EvaluationTask.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/start", response_model=TaskResponse)
async def start_task(task_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EvaluationTask).where(EvaluationTask.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status not in ("pending", "paused"):
        raise HTTPException(status_code=400, detail=f"Task status is {task.status}, cannot start")
    from app.core.benchmark_runner import run_benchmark_task
    from app.db.base import AsyncSessionLocal
    async def _run():
        async with AsyncSessionLocal() as session:
            await run_benchmark_task(task_id, session)
    background_tasks.add_task(_run)
    return task
