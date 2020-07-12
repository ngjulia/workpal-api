# project/app/models/pydantic.py

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
    email: EmailStr
    phone: str
    
class UserOut(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    phone: str
    tasks: List[Task] = []
    
class TaskIn(BaseModel):
    name: str
    description: str
    rank: int
    completed: bool
    completion_time = int
    user_id = int

class TaskOut(BaseModel):
    name: str
    description: str
    rank: int
    completed: bool
    completion_time = int
    created_at = str
    user_id = int

