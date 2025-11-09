from fastapi import APIRouter, status, Path
from db.init_db import db_dependcy
from db.models import Todos
from errors import UNAUTHORIZED, TodoNotFound
from utils.jwt import user_dependency
from schema.input_ import TodoRequest

router = APIRouter(
    tags=["todos"]
    , prefix="/todos"
)


@router.get("/")
async def read_all(user=user_dependency, db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    return db.query(Todos).filter(Todos.owner_id==user.user_id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(todo_id: int = Path(gt=0),user = user_dependency, db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    todo_model = db.query(Todos).filter(Todos.owner_id==user.user_id,Todos.id==todo_id).first()

    if todo_model is not None:
        return todo_model

    raise TodoNotFound


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_req: TodoRequest, user = user_dependency,
                      db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED

    todo_model = Todos(**todo_req.model_dump(), owner_id=user.user_id)

    db.add(todo_model)
    db.commit()


@router.put("/updatetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo( todo_req: TodoRequest, todo_id: int = Path(gt=0), user=user_dependency, db=db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    todo_model = db.query(Todos).filter(Todos.owner_id==user.user_id, Todos.id==todo_id).first()

    if todo_model is None:
        raise TodoNotFound
    
    todo_model.title = todo_req.title # type: ignore
    todo_model.description = todo_req.description # type: ignore
    todo_model.priority = todo_req.priority # type: ignore
    todo_model.complete = todo_req.complete # type: ignore

    db.add(todo_model)
    db.commit()


@router.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(gt=0), user=user_dependency, db = db_dependcy):
    if user is None:
        raise UNAUTHORIZED
    
    todo_model = db.query(Todos).filter(Todos.id==todo_id, Todos.owner_id==user.user_id).first()

    if todo_model is None:
        raise TodoNotFound

    db.query(Todos).filter(Todos.id==todo_id, Todos.owner_id==user.user_id).delete()
    db.commit()