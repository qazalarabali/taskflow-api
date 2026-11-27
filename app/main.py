
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


# CONFIGURATION
app = FastAPI(
    title="TaskFlow API",
    description="A Task Management REST API",
    version="1.0.0"
)

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
tasks_db = []

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
def create_task(task: TaskCreate):
    task_data = task.model_dump()
    task_data["id"] = max(
        (item["id"] for item in tasks_db),
        default=0
    ) + 1

    tasks_db.append(task_data)

    return {
        "message": "Task created successfully",
        "task": task_data
    }

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": tasks_db
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
