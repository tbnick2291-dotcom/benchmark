from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    name: str
    dimension: str
    task_type: str
    config: dict | None = None


class TaskResponse(BaseModel):
    id: int
    name: str
    dimension: str
    task_type: str
    config: dict | None
    status: str
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}
