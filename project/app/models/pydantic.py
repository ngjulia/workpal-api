# project/app/models/pydantic.py
from typing import Optional, List
from pydantic import BaseModel, AnyHttpUrl


#class SummaryPayloadSchema(BaseModel):
#    url: AnyHttpUrl
#
#
#class SummaryResponseSchema(SummaryPayloadSchema):
#    id: int
#
#
#class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
#    summary: str

class UserIn(BaseModel):
    full_name: Optional[str] = None
    email: str
    phone: str
    username: str
    disabled: bool
    
class UserOut(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    phone: str
    tasks: List[str]
    username: str
    disabled: bool
    hashed_password: str

class UserAuth(UserIn):
    password: str

class TaskIn(BaseModel):
    name: str
    rank: int
    completed: bool
    completion_time: int
    user_id = int
    tags: str
    timer: int

class TaskOut(BaseModel):
    id: int
    name: str
    rank: int
    completed: bool
    completion_time: int
    user_id: int
    tags: str
    timer: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None