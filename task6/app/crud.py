from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserLogin
from .security import get_password_hash, verify_password
from .auth import create_access_token

async def username_exists(username: str, session: AsyncSession) -> bool:
    res = await session.execute(select(User).where(User.username == username))
    return res.scalar_one_or_none() is not None

async def register_user(data: UserCreate, session: AsyncSession) -> User:
    if await username_exists(data.username, session):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=data.username,
        password=get_password_hash(data.password),
        role="user"
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def login_user(data: UserLogin, session: AsyncSession) -> dict:
    res = await session.execute(select(User).where(User.username == data.username))
    user = res.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

async def list_users(session: AsyncSession) -> list[User]:
    res = await session.execute(select(User))
    return res.scalars().all()
