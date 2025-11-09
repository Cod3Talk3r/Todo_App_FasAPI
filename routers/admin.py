from fastapi import APIRouter, status, Path
from db.init_db import db_dependcy
from db.models import Todos, UserRole
from errors import UNAUTHORIZED, TodoNotFound
from utils.jwt import user_dependency

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/todos")
async def read_all_admin(user=user_dependency, db=db_dependcy):
    if user is None or user.user_role != UserRole.admin:
        raise UNAUTHORIZED
    
    return db.query(Todos).all()


@router.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete(todo_id: int = Path(gt=0), user=user_dependency, db=db_dependcy):
    if user is None or user.user_role != UserRole.admin:
        raise UNAUTHORIZED
    
    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()

    if todo_model is None:
        raise TodoNotFound
    
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()