from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.db.models import Model
from app.schemas.models import ModelCreate, ModelResponse, ModelStatusUpdate

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=list[ModelResponse])
async def list_models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model))
    return result.scalars().all()


@router.post("", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(payload: ModelCreate, db: AsyncSession = Depends(get_db)):
    model = Model(**payload.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.patch("/{model_id}/status", response_model=ModelResponse)
async def update_model_status(model_id: int, payload: ModelStatusUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    model.status = payload.status
    await db.commit()
    await db.refresh(model)
    return model
