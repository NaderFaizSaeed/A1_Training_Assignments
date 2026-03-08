from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import task as task_model
from ..schemas import task as task_schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=task_schema.Task)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    new_task = task_model.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        project_id=task.project_id,
        assigned_user_id=task.assigned_user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[task_schema.Task])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(task_model.Task).all()

@router.get("/{task_id}", response_model=task_schema.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=task_schema.Task)
def update_task(task_id: int, task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.project_id = task.project_id
    db_task.assigned_user_id = task.assigned_user_id
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}