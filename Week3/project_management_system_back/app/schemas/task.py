from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = "TODO"
    project_id: int
    assigned_user_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True