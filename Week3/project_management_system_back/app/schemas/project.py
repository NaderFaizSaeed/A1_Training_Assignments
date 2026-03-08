from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str
    description: str | None = None
    owner_id: int

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True