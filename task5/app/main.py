from fastapi import FastAPI, Depends
from .database import init_db, get_session
from .schemas import UserCreate, UserLogin, UserOut
from .crud import register_user, login_user
from .auth import get_current_user
from .models import User

app = FastAPI(title="Notes-API Demo", version="1.0")

@app.on_event("startup")
async def _startup():
    await init_db()

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate, session=Depends(get_session)):
    return await register_user(user, session)

@app.post("/login")
async def login(user: UserLogin, session=Depends(get_session)):
    return await login_user(user, session)

@app.get("/users/me", response_model=UserOut)
async def read_me(current: User = Depends(get_current_user)):
    return current
