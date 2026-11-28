
from pydantic import BaseModel

# TASK SCHEMAS
# Define the structure and validation rules for task data.
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

class TaskPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
