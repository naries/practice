from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi_restful.guid_type import GUID, GUID_DEFAULT_SQLITE

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(GUID, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
