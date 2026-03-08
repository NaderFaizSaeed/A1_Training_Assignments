from fastapi import FastAPI
from .database import Base, engine

# IMPORTANT: import models
from .models import user
from .models import project
from .models import task

from .routers import user as user_router
from .routers import project as project_router
from .routers import task as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Management System")

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(project_router.router, prefix="/projects", tags=["Projects"])
app.include_router(task_router.router, prefix="/tasks", tags=["Tasks"])