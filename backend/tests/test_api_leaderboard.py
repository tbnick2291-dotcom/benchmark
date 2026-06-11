import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.asyncio
async def test_leaderboard_overall_empty(client):
    response = await client.get("/api/v1/leaderboard")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_leaderboard_by_dimension(client):
    response = await client.get("/api/v1/leaderboard?dimension=knowledge")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
