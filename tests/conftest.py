#conftest

import os
import pytest
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, DATABASE_URL,SessionLocal
from routers.auth import UserDB
from main import app
import uuid


# Set the environment variable for the duration of the test~s
os.environ["ENV"] = "TEST"

@pytest.fixture(scope="function")
def db_session():
    # Create the test database and initialize the schema
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    # Create a session for the test database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Yield the session to the tests
    yield session

    # Clean up the test database after the tests
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
async def register_user():
    # Generate a unique username for testing
    unique_username = "testuser_" + str(uuid.uuid4())
    
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/register", data={
            "username": unique_username,
            "password": "password",
            "email": f"{unique_username}@email.com",
            "first_name": "Test",
            "last_name": "User"
        })
    with SessionLocal() as db:
        user = db.query(UserDB).filter(UserDB.username == unique_username).first()

        # Print user details
        if user:
            print(f"User ID: {user.id}, Username: {user.username}, API Key: {user.api_key}")
        else:
            print(f"No user found with username: {unique_username}")

        # Print all users in the database
        all_users = db.query(UserDB).all()
        for u in all_users:
            print(f"User in DB - ID: {u.id}, Username: {u.username}, API Key: {u.api_key}")

    return {"api_key": user.api_key, "user_id": user.id}
