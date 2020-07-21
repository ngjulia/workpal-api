from app.models.pydantic import UserIn, TaskIn, UserOut, TaskOut
from app.models.tortoise import User, Task
from typing import Union, List
import json
from datetime import datetime

"""
originally thought that it would make sense to address users by their full name 
and tasks by their name, but those things may not be unique... so using ID for now
"""

# Create
async def post_user(payload: UserIn) -> int:
    print(payload.full_name)
    user = User(full_name=payload.full_name, email=payload.email, phone=payload.phone)
    await user.save() # how does this function work? -> creates/Updates the current model object
    return user.id

async def post_task(payload: TaskIn, user:UserOut) -> int:
    task = await Task.create(name=payload.name, rank=payload.rank, completed=payload.completed, completion_time=payload.completion_time, user_id_id = user['id'])
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
            task['created_at'] = task['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
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
        task['created_at'] = task['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
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
async def put_user(id: int, payload: UserIn) -> Union[dict, None]:
    user = await User.filter(id=id).update(
        full_name=payload.full_name, email=payload.email, phone=payload.phone,
    )
    if user:
        updated_user = await User.filter(id=id).first().values()
        return updated_user[0]
    return None

async def put_task(id: int, task_id: int, payload: TaskIn) -> Union[dict, None]:
    print(payload)
    task = await Task.filter(id=task_id).update(
        name=payload.name, rank=payload.rank, completed=payload.completed, completion_time=payload.completion_time
    )
    if task:
        updated_task = await Task.filter(id=task_id).first().values()
        return updated_task[0]
    return None