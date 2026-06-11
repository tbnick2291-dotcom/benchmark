from pydantic import BaseModel
from datetime import datetime


class ReportGenerateRequest(BaseModel):
    model_id: int
    task_ids: list[int]
    report_type: str = "full"


class ReportResponse(BaseModel):
    id: int
    model_id: int
    task_ids: list[int] | None
    report_type: str | None
    content: dict | None
    generated_at: datetime

    model_config = {"from_attributes": True}
