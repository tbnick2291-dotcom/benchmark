import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.asyncio
async def test_list_tasks_empty(client):
    response = await client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_task(client):
    payload = {
        "name": "knowledge-battle",
        "dimension": "knowledge",
        "task_type": "adversarial",
        "config": {"model_ids": [], "rounds": 3},
    }
    response = await client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["dimension"] == "knowledge"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_get_task_not_found(client):
    response = await client.get("/api/v1/tasks/9999")
    assert response.status_code == 404
