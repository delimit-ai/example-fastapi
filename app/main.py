from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="TaskForge API", version="1.0.0")


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    created_at: datetime
    assignee: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee: Optional[str] = None


tasks_db = {}


@app.get("/api/tasks", response_model=list[Task])
def list_tasks(status: Optional[str] = None):
    """List all tasks, optionally filtered by status."""
    tasks = list(tasks_db.values())
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    return tasks


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    """Create a new task."""
    task_id = len(tasks_db) + 1
    new_task = {
        "id": task_id,
        **task.dict(),
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    tasks_db[task_id] = new_task
    return new_task


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a task by ID."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "uptime": 42}
