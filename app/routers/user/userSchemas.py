# Pydantic
from pydantic import BaseModel, EmailStr, Field

# Date Time
from datetime import datetime

# Typing
from typing import Union, List

"""
****************************************************************************************
                            User Schemas  
****************************************************************************************
"""


"""
************** 
User Output
**************
"""


# User Out
class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


# User Out
class UserOut1(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: str
    created_at: datetime
    # User_details: List[TeacherUser] = []

    class Config:
        orm_mode = True


"""
************** 
Create User
**************
"""


# Create User
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    phone: str
    password: str


"""
************** 
Update User
**************
"""


# Update User
class UserUpdate(BaseModel):
    first_name: Union[str, None]
    last_name: Union[str, None]
    email: Union[EmailStr, None]
    username: Union[str, None]
    phone: Union[str, None]


"""
************** 
Change Password 
**************
"""


class UpdatePassword(BaseModel):
    oldPassword: str
    newPassword: str


"""
************** 
Admin User OutPut
**************
"""


class AdminUserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    is_superadmin: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True
