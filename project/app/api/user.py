from fastapi import APIRouter, HTTPException, Path, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.api import restapi
from app.models.pydantic import (
    UserIn,
    UserOut,
    UserAuth,
    TaskIn,
    TaskOut,
    Token,
    TokenData
)
from app.models.tortoise import UserSchema, TaskSchema
from typing import List, Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    user_id = await restapi.get_id_from_username(username)
    user = await restapi.get_user(user_id)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user

SECRET_KEY = "57dea92282575c0fd58b064b9d9813dc61c1ca3468a862a2881f8a0e43a365b3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_id = await restapi.get_id_from_username(username=token_data.username)
    user = await restapi.get_user(user_id)
    if user is None:
        raise credentials_exception
    print(user)
    return user

async def get_current_active_user(current_user: UserOut = Depends(get_current_user)):
    if current_user['disabled']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.get("/user/me/", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_active_user)):
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

    # -------------------------------------------------------------------

# POST 
@router.post("/user/", response_model=UserOut, status_code=201)
async def create_user(payload: UserAuth) -> UserOut:
    user_id = await restapi.post_user(payload)

    response_object = {
        "id": user_id,
        "full_name": payload.full_name, 
        "email": payload.email, 
        "phone": payload.phone, 
        "username": payload.username, 
        "disabled": False,
        "tasks":[]
    }
    return response_object

@router.post("/user/{id}/task/", response_model=TaskOut, status_code=201)
async def create_task(payload: TaskIn, id: int = Path(..., gt=0)) -> TaskOut:
    user = await restapi.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task_id = await restapi.post_task(payload, user)

    response_object = {"id": task_id, "name":payload.name, "rank":payload.rank, "completed":payload.completed, "completion_time":payload.completion_time, "tags": payload.tags, "timer":payload.timer, "user_id": id}
    return response_object

# GET
@router.get("/user/{id}/", response_model=UserOut)
async def read_user(id: int = Path(..., gt=0)) -> UserOut:
    user = await restapi.get_user(id)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/user/{id}/task/{task_id}/", response_model=TaskOut)
async def read_task(id: int = Path(..., gt=0), task_id: int = Path(..., gt=0)) -> TaskOut:
    task = await restapi.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task['user_id'] = id
    return task

@router.get("/user/", response_model=List[UserOut])
async def read_all_users() -> List[UserOut]:
    return await restapi.get_all_users()

@router.get("/user/{id}/task/", response_model=List[TaskOut])
async def read_all_tasks(id: int = Path(..., gt=0)) -> List[TaskOut]:
    return await restapi.get_all_tasks(id)

# DELETE
@router.delete("/user/{id}/", response_model=UserOut)
async def delete_user(id: int = Path(..., gt=0)) -> UserOut:
    user = await restapi.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await restapi.delete_user(id)

    return user

@router.delete("/user/{id}/task/{task_id}/", response_model=TaskOut)
async def delete_task(id: int = Path(..., gt=0), task_id: int=Path(..., gt=0)) -> TaskOut:
    task = await restapi.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await restapi.delete_task(task_id)
    task['user_id'] = id
    return task

@router.put("/user/{id}/", response_model=UserSchema)
async def update_user(
    payload: UserAuth, id: int = Path(..., gt=0)
) -> UserSchema:
    user = await restapi.put_user(id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/user/{id}/task/{task_id}/", response_model=TaskOut)
async def update_task(
    payload: TaskIn, id: int = Path(..., gt=0), task_id: int = Path(..., gt=0)
) -> TaskOut:
    task = await restapi.put_task(id, task_id, payload)
    print(task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task['user_id'] = id
    return task