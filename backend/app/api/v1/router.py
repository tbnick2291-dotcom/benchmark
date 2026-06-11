from fastapi import APIRouter
from app.api.v1 import models as models_router

router = APIRouter()
router.include_router(models_router.router)
