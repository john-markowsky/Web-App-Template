#test_auth.py

import pytest
import httpx
from main import app
from database import DATABASE_URL
from routers.auth import UserDB, User
from conftest import register_user

@pytest.mark.asyncio
async def test_register(register_user):
    api_key = await register_user
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Test successful registration
        response = await client.post("/register", data={
            "username": "testuser",
            "password": "password",
            "email": "test@email.com",
            "first_name": "Test",
            "last_name": "User"
        })
        assert response.status_code == 303  # Redirect

        # Test for duplicate registration
        response = await client.post("/register", data={
            "username": "testuser",
            "password": "password",
            "email": "test@email.com",
            "first_name": "Test",
            "last_name": "User"
        })
        assert response.status_code == 200  # OK because it's showing the registration page with an error

@pytest.mark.asyncio
async def test_login(register_user):
    api_key = await register_user
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Test successful login
        response = await client.post("/login", data={"username": "testuser", "password": "password"})
        assert response.status_code == 303  # Redirect
        assert response.url == "http://test/login"  # expecting redirect to login on successful login
        
        # Test login with wrong password
        response = await client.post("/login", data={"username": "testuser", "password": "wrongpassword"}, follow_redirects=True)
        assert response.status_code == 200  # OK (serving the login page with error message)
        assert "error=Incorrect%20username%20or%20password" in str(response.url)  # Validate the error message in the final URL

@pytest.mark.asyncio
async def test_logout(register_user):
    api_key = await register_user
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/logout")
        assert response.status_code == 303  # Redirect

@pytest.mark.asyncio
async def test_profile(register_user):
    api_key = await register_user
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/profile")
        # Assuming the user is not logged in for this test
        assert response.status_code == 401