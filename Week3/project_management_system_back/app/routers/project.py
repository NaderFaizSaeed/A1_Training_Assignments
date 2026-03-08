from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import SessionLocal
from ..models import project as project_model
from ..models import task as task_model
from ..models import user as user_model
from ..schemas import project as project_schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=project_schema.Project)
def create_project(project: project_schema.ProjectCreate, db: Session = Depends(get_db)):
    new_project = project_model.Project(
        title=project.title,
        description=project.description,
        owner_id=project.owner_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/", response_model=list[project_schema.Project])
def read_projects(db: Session = Depends(get_db)):
    return db.query(project_model.Project).all()

@router.get("/{project_id}", response_model=project_schema.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(project_model.Project).filter(project_model.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=project_schema.Project)
def update_project(project_id: int, project: project_schema.ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(project_model.Project).filter(project_model.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.title = project.title
    db_project.description = project.description
    db_project.owner_id = project.owner_id
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(project_model.Project).filter(project_model.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@router.get("/{project_id}/details")
def get_project_details(project_id: int, db: Session = Depends(get_db)):
    project = db.query(project_model.Project).options(
        joinedload(project_model.Project.tasks).joinedload(task_model.Task.assigned_user)
    ).filter(project_model.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    result = {
        "project_id": project.id,
        "title": project.title,
        "description": project.description,
        "users": {}
    }
    for task in project.tasks:
     user = task.assigned_user

     if not user:
        continue

     if user.id not in result["users"]:
        result["users"][user.id] = {
            "user_id": user.id,
            "name": user.name,
            "tasks": []
        }

    result["users"][user.id]["tasks"].append({
        "task_id": task.id,
        "title": task.title,
        "status": task.status
    })
    result["users"] = list(result["users"].values())
    return result