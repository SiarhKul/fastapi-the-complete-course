from fastapi import FastAPI

from .models import Base
from .database import engine
from .routers import todos, auth, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/heathy")
def helth_check():
    return {'status':"Heathy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)