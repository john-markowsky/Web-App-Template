#test_user.py

import pytest
import httpx
from main import app

@pytest.mark.asyncio
async def test_dashboard():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/dashboard")
        # Assuming the user is not logged in for this test
        assert response.status_code == 401
