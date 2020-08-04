from fastapi import APIRouter, HTTPException, Path

from app.api import restapi
from app.models.pydantic import (
    UserIn,
    UserOut,
    TaskIn,
    TaskOut,
)
from app.models.tortoise import UserSchema, TaskSchema
from typing import List

router = APIRouter()

# POST 
@router.post("/", response_model=UserOut, status_code=201)
async def create_user(payload: UserIn) -> UserOut:
    user_id = await restapi.post_user(payload)

    response_object = {"id": user_id, "full_name": payload.full_name, "email": payload.email, "phone": payload.phone, "tasks":[]}
    return response_object

@router.post("/{id}/task/", response_model=TaskOut, status_code=201)
async def create_task(payload: TaskIn, id: int = Path(..., gt=0)) -> TaskOut:
    user = await restapi.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task_id = await restapi.post_task(payload, user)

    response_object = {"id": task_id, "name":payload.name, "rank":payload.rank, "completed":payload.completed, "completion_time":payload.completion_time, "tags": payload.tags, "timer":payload.timer, "user_id": id}
    return response_object

# GET
@router.get("/{id}/", response_model=UserOut)
async def read_user(id: int = Path(..., gt=0)) -> UserOut:
    user = await restapi.get_user(id)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{id}/task/{task_id}/", response_model=TaskOut)
async def read_task(id: int = Path(..., gt=0), task_id: int = Path(..., gt=0)) -> TaskOut:
    task = await restapi.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task['user_id'] = id
    return task

@router.get("/", response_model=List[UserOut])
async def read_all_users() -> List[UserOut]:
    return await restapi.get_all_users()

@router.get("/{id}/task/", response_model=List[TaskOut])
async def read_all_tasks(id: int = Path(..., gt=0)) -> List[TaskOut]:
    return await restapi.get_all_tasks(id)

# DELETE
@router.delete("/{id}/", response_model=UserOut)
async def delete_user(id: int = Path(..., gt=0)) -> UserOut:
    user = await restapi.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await restapi.delete_user(id)

    return user

@router.delete("/{id}/task/{task_id}/", response_model=TaskOut)
async def delete_task(id: int = Path(..., gt=0), task_id: int=Path(..., gt=0)) -> TaskOut:
    task = await restapi.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await restapi.delete_task(task_id)
    task['user_id'] = id
    return task

@router.put("/{id}/", response_model=UserSchema)
async def update_user(
    payload: UserIn, id: int = Path(..., gt=0)
) -> UserSchema:
    user = await restapi.put_user(id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/{id}/task/{task_id}/", response_model=TaskOut)
async def update_task(
    payload: TaskIn, id: int = Path(..., gt=0), task_id: int = Path(..., gt=0)
) -> TaskOut:
    task = await restapi.put_task(id, task_id, payload)
    print(task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task['user_id'] = id
    return task