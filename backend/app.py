from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import sqlite3
import os
from src.models.schemas import TaskCreate, TaskUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    # Database is at the root of the backend directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'tasks.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Exception handler to return 400 instead of FastAPI's default 422 for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation error: title cannot be empty"},
    )

@app.get("/api/tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.post("/api/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    # Additional manual check to ensure title is not just whitespace
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (task.title.strip(), task.description)
    )
    task_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    new_task = dict(cursor.fetchone())
    conn.close()
    
    return new_task

@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (task.title.strip(), task.description, task.status, task_id)
    )
    conn.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = dict(cursor.fetchone())
    conn.close()
    
    return updated_task

@app.patch("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    current_status = row['status']
    new_status = 'completed' if current_status == 'pending' else 'pending'
    
    cursor.execute(
        "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_status, task_id)
    )
    conn.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = dict(cursor.fetchone())
    conn.close()
    
    return updated_task

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Task deleted successfully"}
