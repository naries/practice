from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi_restful.guid_type import GUID, GUID_DEFAULT_SQLITE
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")
