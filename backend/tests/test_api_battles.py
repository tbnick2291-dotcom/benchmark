import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.asyncio
async def test_list_battles_empty(client):
    response = await client.get("/api/v1/battles")
    assert response.status_code == 200
    assert response.json() == []
