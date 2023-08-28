#items 

from fastapi import APIRouter, HTTPException, Request, Header, Depends
from sqlalchemy.orm import Session
from typing import Optional,List
from database import Item, SessionLocal
from routers.auth import UserDB, User, get_session, get_db
from sqlalchemy import inspect
from fastapi.templating import Jinja2Templates
from database import ActiveHost
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import datetime

router = APIRouter()

templates = Jinja2Templates(directory="templates")

def authenticate(api_key: str):
    db = SessionLocal()
    user = db.query(UserDB).filter(verify_password(api_key, UserDB.api_key)).first()
    db.close()
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# def validate(user_id, item_data):
    # Check the user ID against your database
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Validate the item data
    # ...

class ActiveHosts(BaseModel):
    api_key: str
    user_id: int
    active_hosts: list[str]

# Define a item data model
class ItemData(BaseModel):
    api_key: str
    user_id: int
    subject: str
    issuer: str
    valid_from: str
    valid_until: str
    status: str

@router.post("/upload_item")
async def upload_item(data: List[ItemData], db: Session = Depends(get_db)):
    # Debugging: Print the received data and its type
    print(f"Received Data: {data}")
    print(f"Type of received API key: {type(data[0].api_key) if data else None}")
    
    # Get the API key from the first item data
    api_key = data[0].api_key if data else None

    # Validate API key and user ID
    user = db.query(UserDB).filter(verify_password(api_key, UserDB.api_key)).first()

    # Debugging: Print the user fetched from the database using the API key
    print(f"User fetched from DB using API key {api_key}: {user}")
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Store item data
    for item_data in data:
        item = Item(
            user_id=item_data.user_id,
            subject=item_data.subject,
            issuer=item_data.issuer,
            status=item_data.status
        )
        item.set_valid_from(item_data.valid_from)
        item.set_valid_until(item_data.valid_until)
        db.add(item)
    db.commit()

    return {"message": "Item data uploaded successfully"}

@router.post("/store_active_hosts")
async def store_active_hosts(data: ActiveHosts, db: Session = Depends(get_db)):
    print(f"Received Data: {data}")  # Print the received data

    # Validate API key and user ID
    user = db.query(UserDB).filter(UserDB.id == data.user_id, UserDB.api_key == data.api_key).first()

    # Print the user fetched from the database
    if user:
        print(f"User from database: {user.username}")
    else:
        print("No matching user found in the database with the provided API key and user ID.")

    if not user:
        print(f"Returning 401 due to invalid API key or user ID.")
        raise HTTPException(status_code=401, detail="Invalid API key or user ID")

    # Store active hosts in the database
    for ip_address in data.active_hosts:
        active_host = ActiveHost(user_id=data.user_id, ip_address=ip_address)
        db.add(active_host)
    db.commit()

    print("Active hosts stored successfully in the database.")
    return JSONResponse(status_code=200, content={"message": "Active hosts stored successfully"})


@router.get("/get_active_hosts")
async def get_active_hosts(api_key: str, db: Session = Depends(get_db)):
    # Debugging: Print the received API key and its type
    print(f"Received API key: {api_key}")
    print(f"Type of received API key: {type(api_key)}")

    user_id = 8  # Hardcode this for now based on the output you provided. Adjust if needed.
    user_by_id = db.query(UserDB).filter(UserDB.id == user_id).first()
    print(f"User fetched by ID: {user_by_id}")
    print(f"API key of user fetched by ID: {user_by_id.api_key}")
    print(f"Input API key: {api_key}")
    print(f"Are API keys identical? {user_by_id.api_key == api_key}")
    
    user = db.query(UserDB).filter(verify_password(api_key, UserDB.api_key)).first()

    # Debugging: Print the user fetched from the database using the API key
    print(f"User fetched from DB using API key {api_key}: {user}")
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    active_hosts = db.query(ActiveHost).filter(ActiveHost.user_id == user.id).all()

    # Debugging: Print the active hosts fetched from the database
    print(f"Active hosts fetched from DB for user ID {user.id}: {active_hosts}")
    
    active_host_ips = [host.ip_address for host in active_hosts]
    return JSONResponse(status_code=200, content={"active_hosts": active_host_ips})
