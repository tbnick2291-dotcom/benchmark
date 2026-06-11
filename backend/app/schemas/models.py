from pydantic import BaseModel
from datetime import datetime


class ModelCreate(BaseModel):
    name: str
    model_path: str
    config: dict | None = None


class ModelResponse(BaseModel):
    id: int
    name: str
    model_path: str
    config: dict | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ModelStatusUpdate(BaseModel):
    status: str
