from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Task title cannot be empty")
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: str
