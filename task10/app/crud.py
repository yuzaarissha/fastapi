from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Note
from .schemas import UserCreate, UserLogin, NoteCreate, NoteUpdate
from .security import get_password_hash, verify_password
from .auth import create_access_token


async def username_exists(username: str, session: AsyncSession) -> bool:
    res = await session.execute(select(User).where(User.username == username))
    return res.scalar_one_or_none() is not None


async def register_user(data: UserCreate, session: AsyncSession) -> User:
    if await username_exists(data.username, session):
        raise HTTPException(400, "Username already exists")
    user = User(
        username=data.username, password=get_password_hash(data.password), role="user"
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def login_user(data: UserLogin, session: AsyncSession) -> dict:
    res = await session.execute(select(User).where(User.username == data.username))
    user = res.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


async def list_users(session: AsyncSession) -> list[User]:
    res = await session.execute(select(User))
    return res.scalars().all()


async def create_note(data: NoteCreate, owner: User, session: AsyncSession) -> Note:
    note = Note(text=data.text, owner_id=owner.id)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


async def get_note(note_id: int, owner: User, session: AsyncSession) -> Note:
    res = await session.execute(
        select(Note).where(Note.id == note_id, Note.owner_id == owner.id)
    )
    note = res.scalar_one_or_none()
    if not note:
        raise HTTPException(404, "Note not found")
    return note


async def list_notes(
    owner: User,
    session: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
) -> list[Note]:
    stmt = select(Note).where(Note.owner_id == owner.id)
    if search:
        stmt = stmt.where(Note.text.ilike(f"%{search}%"))
    stmt = stmt.offset(skip).limit(limit)
    res = await session.execute(stmt)
    return res.scalars().all()


async def update_note(
    note_id: int, data: NoteUpdate, owner: User, session: AsyncSession
) -> Note:
    note = await get_note(note_id, owner, session)
    note.text = data.text
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


async def delete_note(note_id: int, owner: User, session: AsyncSession) -> None:
    note = await get_note(note_id, owner, session)
    await session.delete(note)
    await session.commit()
