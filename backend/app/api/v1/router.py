from fastapi import APIRouter
from app.api.v1 import models as models_router
from app.api.v1 import tasks as tasks_router
from app.api.v1 import battles as battles_router
from app.api.v1 import leaderboard as leaderboard_router
from app.api.v1 import reports as reports_router
from app.api.v1 import system as system_router

router = APIRouter()
router.include_router(models_router.router)
router.include_router(tasks_router.router)
router.include_router(battles_router.router)
router.include_router(leaderboard_router.router)
router.include_router(reports_router.router)
router.include_router(system_router.router)
