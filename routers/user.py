#user.py

from fastapi import APIRouter, HTTPException, Request, Header, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import Item, SessionLocal, ActiveHost
from routers.auth import UserDB, User, get_session, get_db, ActiveHosts
from sqlalchemy import inspect
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard(request: Request, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    username = session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    # Fetch user data from the database
    user_data = db.query(UserDB).filter(UserDB.username == username).first()
    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Fetch user's item data from the database
    item_data = db.query(Item).filter(Item.user_id == user_data.id).all()

    # Fetch user's active hosts data from the database
    active_hosts_data = db.query(ActiveHost).filter(ActiveHost.user_id == user_data.id).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user_data,  # Passing the full user_data object
            "items": item_data,
            "active_hosts": [host.ip_address for host in active_hosts_data]
        }
    )
