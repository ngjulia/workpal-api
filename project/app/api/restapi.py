from app.models.pydantic import UserIn, TaskIn, UserOut, TaskOut, UserAuth
from app.models.tortoise import User, Task
from typing import Union, List
import json
from datetime import datetime
from passlib.context import CryptContext

"""
originally thought that it would make sense to address users by their full name 
and tasks by their name, but those things may not be unique... so using ID for now
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Create
async def post_user(payload: UserAuth) -> int:
    print(payload.full_name)
    user = User(full_name=payload.full_name, email=payload.email, phone=payload.phone, username=payload.username, disabled=payload.disabled, hashed_password=get_password_hash(payload.password))
    await user.save()
    return user.id

async def post_task(payload: TaskIn, user:UserOut) -> int:
    task = await Task.create(name=payload.name, rank=payload.rank, completed=payload.completed, completion_time=payload.completion_time, tags=payload.tags, timer=payload.timer, user_id_id = user['id'])
    await task.save()
    return task.id

# Read
async def get_all_tasks(id: int) -> List:
    tasks = await Task.filter(user_id=id).all().values()
    for task in tasks:
        task['user_id'] = id
    return tasks

async def get_all_users() -> List:
    users = await User.all().values()
    for user in users:
        res = []
        tasks = await Task.filter(user_id=user['id']).all().values()
        for task in tasks:
            task['created_at'] = task['created_at'].strftime("%m/%d/%Y, %H:%M:%S %Z")
            res.append("" + str(task))
        user['tasks'] = res # not sure if this is the right syntax
        # await user.fetch_related('tasks')
        # tasks = user.tasks
        print(user)
    return users

async def get_user(id: int) -> Union[dict, None]:
    user = await User.filter(id=id).first().values()
    tasks = await Task.filter(user_id=id).all().values()
    res = []
    for task in tasks:
        task['created_at'] = task['created_at'].strftime("%m/%d/%Y, %H:%M:%S %Z")
        res.append("" + str(task))
    if user:
        # await user[0].fetch_related('tasks')
        # tasks = user[0].tasks
        user[0]['tasks'] = res # not sure if this is the right syntax
        return user[0]
    return None

async def get_task(id: int) -> Union[dict, None]:
    task = await Task.filter(id=id).first().values()
    if task:
        return task[0]
    return None

# Delete
async def delete_user(id: int) -> int:
    user = await User.filter(id=id).first().delete()
    return user

async def delete_task(id: int) -> int:
    task = await Task.filter(id=id).first().delete()
    return task

# Update
async def put_user(id: int, payload: UserAuth) -> Union[dict, None]:
    user = await User.filter(id=id).update(
        full_name=payload.full_name, email=payload.email, phone=payload.phone, username=payload.username, disabled=payload.disabled, hashed_password=get_password_hash(payload.password)
    )
    if user:
        updated_user = await User.filter(id=id).first().values()
        return updated_user[0]
    return None

async def put_task(id: int, task_id: int, payload: TaskIn) -> Union[dict, None]:
    print(payload)
    task = await Task.filter(id=task_id).update(
        name=payload.name, rank=payload.rank, completed=payload.completed, completion_time=payload.completion_time, tags=payload.tags, timer=payload.timer,
    )
    if task:
        updated_task = await Task.filter(id=task_id).first().values()
        return updated_task[0]
    return None