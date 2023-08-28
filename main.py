#main.py

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils import get_session
from database import Base, engine
from routers import auth, user, items
from routers.auth import get_db, Session, UserDB
import re
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

secret_key = "12345"
app.add_middleware(SessionMiddleware, secret_key=secret_key)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(items.router)

@app.get("/")
async def read_root(request: Request, session: dict = Depends(get_session), db: Session = Depends(get_db)):
    username = session.get("user")
    user_data = None

    if username:
        user_data = db.query(UserDB).filter(UserDB.username == username).first()
    
    return templates.TemplateResponse("index.html", {"request": request, "user": user_data})


# To run with item
# uvicorn main:app --host 0.0.0.0 --port 8000 --secure-keyfile private_key.pem --secure-itemfile item.pem