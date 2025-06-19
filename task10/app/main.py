from fastapi import FastAPI, Depends, Query

from .database import init_db
from .auth import get_current_user, require_role, get_session
from .crud import (
    register_user,
    login_user,
    list_users,
    create_note,
    get_note,
    list_notes,
    update_note,
    delete_note,
)
from .schemas import (
    UserCreate,
    UserLogin,
    UserOut,
    Token,
    NoteCreate,
    NoteUpdate,
    NoteOut,
)
from .models import User

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()


@app.post("/register", response_model=UserOut)
async def register(u: UserCreate, s=Depends(get_session)):
    return await register_user(u, s)


@app.post("/login", response_model=Token)
async def login(u: UserLogin, s=Depends(get_session)):
    return await login_user(u, s)


@app.get("/users/me", response_model=UserOut)
async def me(curr: User = Depends(get_current_user)):
    return curr


@app.get(
    "/admin/users",
    response_model=list[UserOut],
    dependencies=[Depends(require_role("admin"))],
)
async def admin_users(s=Depends(get_session)):
    return await list_users(s)


@app.post("/notes", response_model=NoteOut)
async def add_note(
    n: NoteCreate, curr: User = Depends(get_current_user), s=Depends(get_session)
):
    return await create_note(n, curr, s)


@app.get("/notes", response_model=list[NoteOut])
async def my_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    curr: User = Depends(get_current_user),
    s=Depends(get_session),
):
    return await list_notes(curr, s, skip=skip, limit=limit, search=search)


@app.get("/notes/{note_id}", response_model=NoteOut)
async def read_note(
    note_id: int, curr: User = Depends(get_current_user), s=Depends(get_session)
):
    return await get_note(note_id, curr, s)


@app.put("/notes/{note_id}", response_model=NoteOut)
async def edit_note(
    note_id: int,
    n: NoteUpdate,
    curr: User = Depends(get_current_user),
    s=Depends(get_session),
):
    return await update_note(note_id, n, curr, s)


@app.delete("/notes/{note_id}", status_code=204)
async def remove_note(
    note_id: int, curr: User = Depends(get_current_user), s=Depends(get_session)
):
    await delete_note(note_id, curr, s)
