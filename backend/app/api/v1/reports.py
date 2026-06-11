from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import get_db
from app.db.models import Report
from app.schemas.reports import ReportGenerateRequest, ReportResponse
from app.core.report_generator import save_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=list[ReportResponse])
async def list_reports(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).order_by(Report.generated_at.desc()))
    return result.scalars().all()


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(payload: ReportGenerateRequest, db: AsyncSession = Depends(get_db)):
    report = await save_report(
        model_id=payload.model_id,
        task_ids=payload.task_ids,
        report_type=payload.report_type,
        db=db,
    )
    return report
