from pydantic import BaseModel
from db.models import UserRole

class UserPanel(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str | None
    role: UserRole