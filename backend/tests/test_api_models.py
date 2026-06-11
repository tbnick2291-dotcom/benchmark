import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.asyncio
async def test_list_models_empty(client):
    response = await client.get("/api/v1/models")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_model(client):
    payload = {"name": "test-model", "model_path": "/models/test"}
    response = await client.post("/api/v1/models", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test-model"
    assert data["status"] == "inactive"


@pytest.mark.asyncio
async def test_get_model(client):
    create_resp = await client.post("/api/v1/models", json={"name": "m1", "model_path": "/p"})
    model_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    assert response.json()["id"] == model_id


@pytest.mark.asyncio
async def test_get_model_not_found(client):
    response = await client.get("/api/v1/models/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_model_status(client):
    create_resp = await client.post("/api/v1/models", json={"name": "m2", "model_path": "/p"})
    model_id = create_resp.json()["id"]
    response = await client.patch(f"/api/v1/models/{model_id}/status", json={"status": "active"})
    assert response.status_code == 200
    assert response.json()["status"] == "active"
