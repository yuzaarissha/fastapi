from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str
    role: str = Field(default="user")

    notes: list["Note"] = Relationship(back_populates="owner")

class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    owner_id: int | None = Field(default=None, foreign_key="user.id")

    owner: User | None = Relationship(back_populates="notes")
