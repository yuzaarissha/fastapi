from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config: from_attributes = True

class NoteCreate(BaseModel):
    text: str

class NoteUpdate(BaseModel):
    text: str

class NoteOut(BaseModel):
    id: int
    text: str
    owner_id: int
    class Config: from_attributes = True
