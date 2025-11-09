from fastapi import APIRouter, status
from db.init_db import db_dependcy
from db.models import Users
from routers.auth import password_manager
from errors import UNAUTHORIZED, WrongPassword
from utils.jwt import user_dependency
from schema.output import UserPanel
from schema.input_ import ChangePassword, UpdatePhoneNumber

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/get_user")
async def get_user(user=user_dependency, db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    info = db.query(Users).filter(Users.username==user.username).first()

    return UserPanel(id=info.id, username=info.username, email=info.email, first_name=info.first_name, last_name=info.last_name, role=info.role, phone_number=info.phone_number) # type: ignore


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(passwords: ChangePassword, user=user_dependency, db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    user_model = db.query(Users).filter(Users.username==user.username).first()

    if not password_manager.verify(passwords.old_password, user_model.hashed_password): # type: ignore
        raise WrongPassword
    
    if passwords.new_password != passwords.verify_password:
        raise WrongPassword
    
    hashed_password = password_manager.hash(passwords.new_password)
    user_model.hashed_password = hashed_password # type: ignore

    db.add(user_model)
    db.commit()
    db.refresh(user_model)


@router.put("/addphonenumber", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(data:UpdatePhoneNumber, user=user_dependency, db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    user_model = db.query(Users).filter(Users.id==user.user_id).first()
    user_model.phone_number = data.phone_number # type: ignore

    db.add(user_model)
    db.commit()
    db.refresh(user_model)