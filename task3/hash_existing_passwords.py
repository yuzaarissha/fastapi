import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.database import async_session, init_db
from app.models import User
from app.security import get_password_hash

async def hash_existing_passwords():
    async with async_session() as session:
        users = (await session.execute(select(User))).scalars().all()
        updated = False
        for user in users:
            if not user.password.startswith("$2b$"):
                user.password = get_password_hash(user.password)
                session.add(user)
                updated = True
        if updated:
            await session.commit()

async def main():
    await init_db()
    await hash_existing_passwords()

asyncio.run(main())
