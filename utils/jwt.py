from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schema.jwt import JWTResponsePayload, Payload
from utils.secrets import ALGORITHM, SECRET_KEY, MINET
from utils.settings import password_manager
from db.models import UserRole, Users
from errors import TokenIsNotValid


bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def user_authendication(username, password, db):
    user = db.query(Users).filter(Users.username==username).first()

    if not user:
        return False
    
    if not password_manager.verify(password, user.hashed_password):
        return False
    
    return user


def generate_token(user_id: int, username: str, role: str, expire: timedelta | None = None):
    exp = expire if expire else datetime.now(timezone.utc) + timedelta(minutes=MINET)

    to_code = {
        "sub": username,
        "exp": exp,
        "id": user_id,
        "role": role
    }

    encoded_jwt = jwt.encode(to_code, SECRET_KEY, ALGORITHM)

    return JWTResponsePayload(access_token=encoded_jwt)


async def verify_token(token: str = Depends(bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub") # type: ignore
        user_id: int = payload.get("id") # type: ignore
        user_role: UserRole = payload.get("role") # type: ignore

        if username is None or user_id is None:
            raise TokenIsNotValid
        
        return Payload(username=username, user_id=user_id, user_role=user_role)
    
    except JWTError:
        raise TokenIsNotValid
    

user_dependency: Payload = Depends(verify_token)