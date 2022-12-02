
# Pydantic
from pydantic import BaseModel, EmailStr

# Date Time
from datetime import datetime

# Typing
from typing import Union, List, Dict

# Import  User
from app.routers.category.CategorySchemas import OutCategory

"""
****************************************************************************************
                            Review Question Schemas  
****************************************************************************************
"""


"""
************** 
Review Question - Create
**************
"""


class ReviewQuestion(BaseModel):
    category_id: int
    user_id: int
    question: str


"""
************** 
OUT Review Question  
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


"""
************** 
Update
**************
"""


# Update User
class ReviewQuestionUpdate(BaseModel):
    category_id: Union[int, None]
    user_id: Union[int, None]
    question: Union[str, None]


"""
************** 
OUT Review Question  - Relationship
**************
"""


# class OutCategory1(BaseModel):
#     id: int
#     category_name: str
#     is_active: bool
#     created_at: datetime

#     # re_que: List[OutReviewQuestion] = []

#     class Config:
#         orm_mode = True


# class OutReviewQuestionWithRelationship(BaseModel):
#     id: int
#     category_id: int
#     user_id: int
#     question: str
#     is_active: bool
#     created_at: datetime

#     # categ: List[OutCategory] = []

#     class Config:
#         orm_mode = True


"""
************** 
Create with Relationship 
**************
"""


class CreateCategory(BaseModel):
    category_name: str


class CreateQuestion(BaseModel):
    user_id: int
    question: str


class CreateCateQue(BaseModel):
    category: CreateCategory
    question: CreateQuestion
