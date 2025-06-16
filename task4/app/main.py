from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session, init_db
from .schemas import UserCreate, UserLogin, UserOut
from .crud import register_user, login_user

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

async def get_session():
    async with async_session() as session:
        yield session

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await register_user(user, session)

@app.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    return await login_user(user, session)
