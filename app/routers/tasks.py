
# IMPORTS
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

# ROUTER CONFIGURATION
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# CREATE TASK
@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
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
@router.get("")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    return {
        "tasks": tasks
    }

# GET SINGLE TASK
@router.get("/{task_id}")
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
@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
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


# PATCH TASK
@router.patch("/{task_id}")
def patch_task(
    task_id: int,
    task: schemas.TaskPatch,
    db: Session = Depends(get_db)
):
    db_task = db.get(models.Task, task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task_data = task.model_dump(exclude_unset=True)

    if not task_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field must be provided"
        )

    if any(value is None for value in task_data.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Fields cannot be null"
        )

    for key, value in task_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return {
        "message": "Task updated successfully",
        "task": db_task
    }

# DELETE TASK
@router.delete(
    "/{task_id}",
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