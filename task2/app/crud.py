from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .models import User
from .schemas import UserCreate, UserLogin

async def register_user(user_data: UserCreate, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.username == user_data.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=user_data.username, password=user_data.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def login_user(user_data: UserLogin, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.username == user_data.username))
    user = result.scalar()
    if not user or user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
