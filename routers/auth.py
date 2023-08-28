#auth.py

from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
from passlib.context import CryptContext
from typing import Optional,List
import secrets
from sqlalchemy import inspect
from pydantic import BaseModel
from utils import get_session, get_db, SessionLocal, Base
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import Base, DATABASE_URL

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(session: dict = Depends(get_session)):
    user = session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    job_title = Column(String)
    api_key = Column(String(256), unique=True, index=True)  # Ensure it's a String and has a sufficient length
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# Check if the table exists

inspector = inspect(engine)
tables = inspector.get_table_names()
if "users" not in tables:
    init_db()

# Content from models.py
class User(BaseModel):
    username: str
    hashed_password: str
    email: str
    first_name: str
    last_name: str
    company: Optional[str]
    job_title: Optional[str]

class ActiveHosts(BaseModel):
    api_key: str
    user_id: int
    active_hosts: List[str]


# Content from security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

router = APIRouter()

@router.post("/register")
async def register_out(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    company: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    session: dict = Depends(get_session),
    db: Session = Depends(get_db)
):
    # Check if the username already exists
    existing_user = db.query(UserDB).filter(UserDB.username == username).first()
    if existing_user:
        print(f"User {username} already exists.")
        # Print response details here
        print("Returning 200 OK because username already exists.")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username already exists. Please choose a different one.",
            "user": session.get("user", None)
        })

    hashed_password = get_password_hash(password)
    api_key = get_password_hash(secrets.token_urlsafe(32))  # Generate and hash an API key
    user = UserDB(
        username=username,
        hashed_password=hashed_password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        company=company,
        job_title=job_title,
        api_key=api_key
    )
    db.add(user)
    db.commit()
    session["user"] = username
    print(f"User {username} registered successfully.")
    # Print response details here
    print("Returning 303 Redirect after successful registration.")
    return RedirectResponse(url="/", status_code=303)

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: dict = Depends(get_session),
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    
    # Debugging prints
    if user:
        print(f"User {username} exists in the database.")
    else:
        print(f"User {username} does NOT exist in the database.")
    print(f"Provided Username: {username}")
    print(f"Provided Password: {password}")
    if user:
        print(f"Hashed Password from DB: {user.hashed_password}")
        print(f"Password Verification Result: {verify_password(password, user.hashed_password)}")
    
    if user and verify_password(password, user.hashed_password):
        session["user"] = username
        print(f"Current Session Data: {session}") 
        return RedirectResponse(url="/", status_code=303)
    else:
        error_url = "/login?error=Incorrect%20username%20or%20password"  # Encoded space as %20
        return RedirectResponse(url=error_url, status_code=303)

@router.get("/register")
async def register_in(request: Request, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    username = session.get("user")
    user_data = None
    if username:
        user_data = db.query(UserDB).filter(UserDB.username == username).first()
    return templates.TemplateResponse("register.html", {"request": request, "user": user_data})

@router.get("/login")
async def login_in(request: Request, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    username = session.get("user")
    user_data = None
    if username:
        user_data = db.query(UserDB).filter(UserDB.username == username).first()
    return templates.TemplateResponse("login.html", {"request": request, "user": user_data})


@router.get("/logout")
async def logout(request: Request, session: dict = Depends(get_session)):
    if "user" in session:
        del session["user"]
    return RedirectResponse(url="/", status_code=303)

@router.get("/profile")
async def profile(request: Request, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    username = session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # Fetch user data from the database
    user_data = db.query(UserDB).filter(UserDB.username == username).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user_data})

@router.post("/profile")
async def update_profile(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(None),
    new_email: str = Form(None),
    session: dict = Depends(get_session),
    db: Session = Depends(get_db)
):
    user = session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    # Fetch user data from the database
    user_data = db.query(UserDB).filter(UserDB.username == user).first()

    # Verify the current password
    if not verify_password(current_password, user_data.hashed_password):
        return RedirectResponse(url="/profile?error=Incorrect current password", status_code=303)

    # Update the password if provided
    if new_password:
        user_data.hashed_password = get_password_hash(new_password)

    # Update the email if provided
    if new_email:
        user_data.email = new_email

    db.commit()
    return RedirectResponse(url="/profile?success=Profile updated successfully", status_code=303)
