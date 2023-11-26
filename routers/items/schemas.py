from pydantic import BaseModel
from uuid import UUID


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID
    owner_id: UUID

    class Config:  # used to provide configuration for pydantic.
        from_attributes = True
