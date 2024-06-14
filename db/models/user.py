from sqlmodel import SQLModel, Field, Column, String
from pydantic import EmailStr

from db.utils import generate_id


class UserCreate(SQLModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=8, max_length=16)


class UserLogin(SQLModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=8, max_length=16)


class User(UserCreate, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))
    username: str = Field(sa_column=Column("username", String, unique=True))


class UserRead(SQLModel):
    id: str
    username: str