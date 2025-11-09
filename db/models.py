from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
import enum


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False) # type: ignore
    is_active = Column(Boolean, default=True)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))