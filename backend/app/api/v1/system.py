from fastapi import APIRouter
from app.inference.vllm_client import vllm_client

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/status")
async def system_status():
    try:
        models = await vllm_client.list_models()
        vllm_status = "online"
    except Exception as e:
        models = []
        vllm_status = f"offline: {e}"
    return {"vllm_status": vllm_status, "loaded_models": models}
