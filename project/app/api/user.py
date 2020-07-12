from fastapi import APIRouter, HTTPException, Path

from app.api import restapi
from app.models.pydantic import (
    UserIn,
    UserOut,
    TaskIn,
    TaskOut,
)
from app.models.tortoise import User, Task
from typing import List

router = APIRouter()

# POST 
@router.post("/user", response_model=UserOut, status_code=201)
async def create_user(payload: UserIn) -> UserOut:
    user_id = await restapi.post_user(payload)

    response_object = {"id": user_id, "full_name": payload.full_name, "email": payload.email, "phone": payload.phone, "tasks":[]}
    return response_object

@router.post("/user/{id}/task", response_model=TaskOut, status_code=201)
async def create_task(payload: TaskIn, id: int = Path(..., gt=0)) -> TaskOut:
    task_id = await restapi.post_task(payload)

    response_object = {"id": task_id, "name":payload.name, "description":payload.description, "rank":payload.rank, "completed":payload.completed, "completion_time":payload.completion_time, "user_id": id}
    return response_object

# GET
@router.get("/user/{id}", response_model=UserOut)
async def read_user(id: int = Path(..., gt=0)) -> UserOut:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/user/{id}/task/{task_id}", response_model=TaskOut)
async def read_task(id: int = Path(..., gt=0), task_id: int = Path(..., gt=0)) -> TaskOut:
    task = await crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/user", response_model=List[UserOut])
async def read_all_users() -> List[UserOut]:
    return away crud.get_all_users

@router.get("/user", response_model=List[TaskOut])
async def read_all_tasks() -> List[TaskOut]:
    return away crud.get_all_tasks

# DELETE
@router.delete("/user/{id}", response_model=UserOut)
async def delete_user(id: int = Path(..., gt=0)) -> UserOut:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud.delete_user(id)

    return user

@router.delete("/user/{id}/task/{task_id}", response_model=TaskOut)
async def delete_task(id: int = Path(..., gt=0), task_id: int=Path(..., gt=0)) -> TaskOut:
    task = await crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await crud.delete_task(task_id)

    return task

@router.put("/user/{id}", response_model=UserOut)
async def update_user(
    payload: UserIn, id: int = Path(..., gt=0)
) -> UserOut:
    user = await crud.put_user(id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/user/{id}/task/{task_id}", response_model=TaskOut)
async def update_task(
    payload: TaskIn, id: int = Path(..., gt=0)
) -> TaskOut:
    task = await crud.put_user(task_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="Task not found")

    return task