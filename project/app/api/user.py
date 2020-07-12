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


@router.post("/user", response_model=UserOut, status_code=201)
    async def create_user(payload: UserIn) -> UserOut:
    user_id = await restapi.post_user(payload)

    response_object = {"id": user_id, "full_name": payload.full_name, "email": payload.email, "phone": payload.phone}
    return response_object

@router.post("/user/{id}/task", response_model=TaskOut, status_code=201)
    async def create_task(payload: TaskIn, id: int = Path(..., gt=0)) -> TaskOut:
    task_id = await restapi.post_task(payload)

    response_object = {"id": task_id, "name":payload.name, "description":payload.description, "rank":payload.rank, "completed":payload.completed, "completion_time":payload.completion_time}
    return response_object


