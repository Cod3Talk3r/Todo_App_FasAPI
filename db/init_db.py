from db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


def get_db():
    with SessionLocal() as db:
        yield db


db_dependcy: Session = Depends(get_db)