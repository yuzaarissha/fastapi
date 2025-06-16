import os, datetime as dt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .models import User
from .schemas import UserCreate, UserLogin
from .security import hash_password, verify_password
from .auth import create_access_token

load_dotenv()
TOKEN_TTL = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

async def register_user(data: UserCreate, session: AsyncSession) -> User:
    q = await session.execute(select(User).where(User.username == data.username))
    if q.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=data.username, password=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def login_user(data: UserLogin, session: AsyncSession):
    q = await session.execute(select(User).where(User.username == data.username))
    user: User | None = q.scalar()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    token = create_access_token(user.username, TOKEN_TTL)
    return {"access_token": token, "token_type": "bearer"}
