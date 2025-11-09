from pydantic import BaseModel, Field
from db.models import UserRole

class UserInput(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    hashed_password: str
    role: UserRole


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class UpdatePhoneNumber(BaseModel):
    phone_number: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    verify_password: str