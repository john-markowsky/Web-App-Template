#test_main.py

import pytest
import httpx
from main import app
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_read_root():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Test the root endpoint
        response = await client.get("/")
        assert response.status_code == 200
        # You can add more assertions based on the content of index.html
        
        # Test the root endpoint with a simulated logged-in session
        cookies = {"user": "testuser"}  # Simulate a logged-in session
        response = await client.get("/", cookies=cookies)
        assert response.status_code == 200
        # You can also add more assertions based on the content of index.html when a user is logged in

@pytest.mark.asyncio
async def test_startup():
    # This test will ensure the startup event runs without errors.
    # If there's an error in the startup event, the test will fail.
    with TestClient(app) as client:  # This will trigger the startup event
        pass
