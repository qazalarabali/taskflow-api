
# IMPORTS
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

# DATABASE INITIALIZATION
# Create database tables based on the defined SQLAlchemy models.
Base.metadata.create_all(bind=engine)

# SCHEMAS
# Define the structure and validation rules for incoming task data.
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

# ENDPOINTS
# Basic API endpoints for project information and health checks.

# ROOT
@app.get("/")
def root():
    return {
        "message": "Welcome to TaskFlow API!",
        "status": "success"
    }

# HEALTH CHECK
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
    
# ABOUT
@app.get("/about")
def about():
    return {
        "project": "TaskFlow API",
        "version": "1.0.0",
        "description": "Task Management Backend"
    }

# TASK ENDPOINTS
# CRUD operations for managing tasks in PostgreSQL.

# CREATE TASK
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

# GET ALL TASKS
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    return {
        "tasks": tasks
    }

# GET SINGLE TASK
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.get(models.Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "task": db_task
    }

# UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    db_task = db.get(models.Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task_data = task.model_dump()

    for key, value in task_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return {
        "message": "Task updated successfully",
        "task": db_task
    }

# DELETE TASK
@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.get(models.Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(db_task)
    db.commit()

    return

# DATABASE CHECK
# Verify the connection between FastAPI and PostgreSQL.
@app.get("/db-check")
def database_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "status": "success"
    }
