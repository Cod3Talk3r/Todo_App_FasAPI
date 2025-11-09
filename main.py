from fastapi import FastAPI
import db.models as models
from db.database import engine
from routers import auth, todos, admin, user

app = FastAPI()

@app.on_event("startup")
async def start_up():
    models.Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health():
    return {"status:": "Healthy"}
    

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)