import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root_returns_200():
    async with AsyncClient(app=app, base_url="http://www.google.com") as client:
        response = await client.get("/")
    assert response.status_code == 200
