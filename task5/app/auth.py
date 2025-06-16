import os, datetime as dt
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .database import get_session
from .models import User

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM")

bearer_scheme = HTTPBearer()

def create_access_token(sub: str, minutes: int) -> str:
    exp = dt.datetime.utcnow() + dt.timedelta(minutes=minutes)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials
    auth_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise auth_err
    except JWTError:
        raise auth_err

    result = await session.execute(select(User).where(User.username == username))
    user: User | None = result.scalar()
    if user is None:
        raise auth_err
    return user
