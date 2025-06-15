from .models import User
from .schemas import UserCreate, UserLogin
from .security import get_password_hash, verify_password
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

async def register_user(user_data: UserCreate, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.username == user_data.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def login_user(user_data: UserLogin, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.username == user_data.username))
    user = result.scalar()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
