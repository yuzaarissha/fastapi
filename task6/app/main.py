from fastapi import FastAPI, Depends

from .database import init_db
from .auth import get_current_user, require_role, get_session
from .crud import register_user, login_user, list_users
from .schemas import UserCreate, UserLogin, UserOut, Token
from .models import User

app = FastAPI(title="Notes API with Roles")

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate, session=Depends(get_session)):
    return await register_user(user, session)

@app.post("/login", response_model=Token)
async def login(user: UserLogin, session=Depends(get_session)):
    return await login_user(user, session)

@app.get("/users/me", response_model=UserOut)
async def read_me(current: User = Depends(get_current_user)):
    return current

@app.get("/admin/users", response_model=list[UserOut],
         dependencies=[Depends(require_role("admin"))])
async def admin_users(session=Depends(get_session)):
    return await list_users(session)
