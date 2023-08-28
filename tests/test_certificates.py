import pytest
import httpx
from conftest import register_user
from main import app
import datetime

@pytest.mark.asyncio
async def test_upload_item(register_user):  
    user_data = await register_user
    api_key = user_data["api_key"]
    user_id = user_data["user_id"]
    print(f"API Key from fixture: {api_key}")
    print(f"User ID from fixture: {user_id}")

    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        data = [{
            "api_key": api_key,
            "user_id": user_id,
            "subject": "Test Subject",
            "issuer": "Test Issuer",
            "valid_from": datetime.date(2023, 1, 1).isoformat(),
            "valid_until": datetime.date(2023, 12, 31).isoformat(),
            "status": "Valid"
        }]

        response = await client.post("/upload_item", json=data)
        print(f"Upload Item Response Body: {response.text}")  # Print the response body
        assert response.status_code == 200



@pytest.mark.asyncio
async def test_store_active_hosts(register_user):  
    user_data = await register_user
    api_key = user_data["api_key"]
    user_id = user_data["user_id"]
    print(f"API Key from fixture: {api_key}")
    print(f"User ID from fixture: {user_id}")
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        data = {
            "api_key": api_key,
            "user_id": user_id,
            "active_hosts": ["192.168.0.1"]
        }
        response = await client.post("/store_active_hosts", json=data)
        print(f"Response Body: {response.text}")  # Print the response body
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_active_hosts(register_user):  
    api_key = await register_user
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/get_active_hosts?api_key={api_key['api_key']}")
        print(f"Get Active Hosts Response Body: {response.text}")  # Print the response body
        assert response.status_code == 200

