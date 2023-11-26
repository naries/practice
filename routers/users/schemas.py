from pydantic import BaseModel
from routers.items import schemas
from uuid import UUID


class UserBase(BaseModel):
    username: str


class UserChangeStatus(UserBase):
    password: str


class UserCreate(UserBase):
    email: str
    password: str
    full_name: str


class User(UserBase):
    id: UUID
    email: str
    disabled: bool
    items: list[schemas.Item] = []

    class Config:
        from_attributes = True
