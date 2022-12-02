# Pydantic
from pydantic import BaseModel, EmailStr, Field

# Date Time
from datetime import datetime

# Typing
from typing import Union, List

# Import User Schemas
from app.routers.user import userSchemas


"""
****************************************************************************************
                            Category Schemas  
****************************************************************************************
"""


"""
************** 
Category Base
**************
"""


class CreateCategory(BaseModel):
    category_name: str


"""
************** 
Get Category 
**************
"""


class OutCategory(BaseModel):
    id: int
    category_name: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


"""
************** 
Update
**************
"""


# Update User
class CategoryUpdate(BaseModel):
    category_name: Union[str, None]


"""
************** 
Get With Realtionship
**************
"""


class OutReviewQuestion(BaseModel):
    id: int
    category_id: int
    user_id: int
    question: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class OutCategory1(BaseModel):
    id: int
    category_name: str
    is_active: bool
    created_at: datetime

    re_que: List[OutReviewQuestion] = []

    class Config:
        orm_mode = True
