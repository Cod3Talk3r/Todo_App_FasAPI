from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from db.init_db import db_dependcy
from db.models import Users
from errors import UserNotFound, ExistingEmail, ExistingUser
from utils.settings import password_manager
from schema.jwt import JWTResponsePayload
from utils.jwt import user_authendication, generate_token
from schema.input_ import UserInput

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserInput, db = db_dependcy):
    existing_user = db.query(Users).filter(Users.username == data.username).first()
    existing_email = db.query(Users).filter(Users.email == data.email).first()

    if existing_user:
        raise ExistingUser
    
    if existing_email:
        raise ExistingEmail

    pwd = password_manager.hash(data.hashed_password)
    data.hashed_password = pwd
    user_model = Users(**data.model_dump())

    db.add(user_model)
    db.commit()
    db.refresh(user_model)


@router.post("/token", response_model=JWTResponsePayload)
async def create_token(data: OAuth2PasswordRequestForm = Depends(), db = db_dependcy):
    user = user_authendication(data.username, data.password, db)

    if not user:
        raise UserNotFound
    
    token = generate_token(user.id, user.username, user.role.value) # type: ignore

    return token