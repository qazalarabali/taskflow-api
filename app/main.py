
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sqlalchemy import text
from app.database import engine, Base, get_db
from app import models

# CONFIGURATION
app = FastAPI(
    title="TaskFlow API",
    description="A Task Management REST API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# SCHEMAS
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

# DATABASE
# tasks_db = []

# ENDPOINTS
@app.get("/")
def root():
    return {
        "message": "Welcome to TaskFlow API!",
        "status": "success"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/about")
def about():
    return {
        "project": "TaskFlow API",
        "version": "1.0.0",
        "description": "Task Management Backend"
    }

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return {
        "message": "Task created successfully",
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed
        }
    }

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    return {
        "tasks": tasks
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next(
        (item for item in tasks_db if item["id"] == task_id),
        None
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "task": task
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    for index, existing_task in enumerate(tasks_db):
        if existing_task["id"] == task_id:
            updated_task = task.model_dump()
            updated_task["id"] = task_id

            tasks_db[index] = updated_task

            return {
                "message": "Task updated successfully",
                "task": updated_task
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

# DATABASE CHECK
@app.get("/db-check")
def database_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "status": "success"
    }