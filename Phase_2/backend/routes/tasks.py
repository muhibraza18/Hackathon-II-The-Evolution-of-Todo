from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from db import get_session
from auth import get_current_user_id

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    # Create task instance with validated data and current user ID
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user_id  # Assign task to current authenticated user
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user
    """
    tasks = session.exec(select(Task).where(Task.user_id == current_user_id)).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a task for the authenticated user
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/toggle-complete", response_model=TaskResponse)
def toggle_complete(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the authenticated user
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to modify it"
        )
    if task.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to modify it"
        )

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task