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
    
class UserOut(BaseModel):
    full_name: Optional[str] = None
    email: str
    phone: str
    tasks: List[str]
    
class TaskIn(BaseModel):
    name: str
    description: str
    rank: int
    completed: bool
    completion_time: int
    # user_id = int

class TaskOut(BaseModel):
    name: str
    description: str
    rank: int
    completed: bool
    completion_time: int
    created_at: str
    user_id: int

