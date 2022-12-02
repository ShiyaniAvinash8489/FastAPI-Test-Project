from unicodedata import category
from fastapi import (status,
                     Depends,
                     APIRouter,
                     Request,
                     templating,
                     responses,
                     )

from pydantic import EmailStr
from requests import request

# SQlAlchemy ORM
from sqlalchemy.orm import Session

# Import Modules
from app import models

# Import database Settings
from app.db_connection import get_db
from app import db_connection

# Schemas
from app.routers.category import CategorySchemas

# Response
from fastapi.responses import HTMLResponse

# Permission For API
from app.routers.authentication.oAuth2 import authenticated_permission,  admin_permission

# typing
from typing import List, Optional

# Regex
import re

# Validation
from app import Regex_validation

"""
****************************************************************************************
                                    Router Setting
****************************************************************************************
"""


# Routers Settings
router = APIRouter(
    prefix="/Category",
    tags=['Category']
)


"""
****************************************************************************************
                                    Custom Error Handling
****************************************************************************************
"""


# Custom Error Handling
class Custom_Validation_Category(Exception):
    def __init__(self, name: str):
        self.name = name


"""
****************************************************************************************
                                    CRUD  Categpry
****************************************************************************************
"""


"""
**************
Create 
**************
"""


# Create Category with Regex validation (Allow Alphabet and White Space)
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(ctr: CategorySchemas.CreateCategory, db: Session = Depends(get_db), auth_permission: int = Depends(admin_permission)):

    # Regex Validation
    Regex_validation.name_Regex(name=ctr.category_name)

    new_category = models.Category(**ctr.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    CategoryData = {
        "id": new_category.id,
        "category_name": new_category.category_name,
        "is_active": new_category.is_active,
        "created_at": new_category.created_at
    }

    # return new_user
    return {
        "response_code": 201,
        "response_message": "Category have been created.",
        "response_data": CategoryData,
    }


"""
**************
Bulk Create
**************
"""


# Create Category with Regex validation (Allow Alphabet and White Space)
@router.post("/create-Bulk", status_code=status.HTTP_201_CREATED)
def create_category_bilk(ctr: List[CategorySchemas.CreateCategory], db: Session = Depends(get_db)):

    Objects = []
    for category in ctr:

        Regex_validation.name_Regex(name=category.category_name)

        new_category = models.Category(**category.dict())
        Objects.append(new_category)

    db.bulk_save_objects(Objects)
    db.commit()

    return {
        "response_code": 201,
        "response_message": "Category have been created.",
        "response_data": Objects,
    }


"""
**************
Get All 
**************
"""


# Get All Category with Ascending order by ID
@router.get(path="/get_all", status_code=status.HTTP_200_OK, response_model=List[CategorySchemas.OutCategory])
def get_all(database: Session = Depends(get_db), auth_permission: int = Depends(authenticated_permission)):
    category = database.query(models.Category).filter(
        models.Category.is_active == True).order_by(models.Category.id).all()
    return category


# With Relation Ship
@router.get(path="/get_all_relationship", status_code=status.HTTP_200_OK, response_model=List[CategorySchemas.OutCategory1])
def get_all_relationship(database: Session = Depends(get_db), auth_permission: int = Depends(authenticated_permission)):
    category = database.query(models.Category).filter(
        models.Category.is_active == True).order_by(models.Category.id).all()
    return category


"""
**************
Get single
**************
"""


# Get Specific Category
@router.get(path="/{id}", status_code=status.HTTP_200_OK)
def get_category(id: int, db: Session = Depends(get_db), auth_permission: int = Depends(authenticated_permission)):

    category = db.query(models.Category).filter(
        models.Category.id == id, models.Category.is_active == True).first()

    if not category:
        raise Custom_Validation_Category(name=f"Category does not exist.")

    Data = {
        "id": category.id,
        "category_name": category.category_name,
        "is_active": category.is_active,
        "created_at": category.created_at
    }

    return {
        "response_code": 200,
        "response_message": "Success",
        "response_data": Data
    }


# With Relationship
@router.get(path="/Relationship/{id}", status_code=status.HTTP_200_OK)
def get_category(id: int, db: Session = Depends(get_db), auth_permission: int = Depends(authenticated_permission)):

    category = db.query(models.Category).filter(
        models.Category.id == id, models.Category.is_active == True).first()

    if not category:
        raise Custom_Validation_Category(name=f"Category does not exist.")

    Data = {
        "id": category.id,
        "category_name": category.category_name,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "Question": category.re_que
    }

    return {
        "response_code": 200,
        "response_message": "Success",
        "response_data": Data
    }


"""
**************
Update
**************
"""


# Update Category
@router.patch("/Update", status_code=status.HTTP_200_OK, )
def Update_Category(id: int, category: CategorySchemas.CategoryUpdate, db: Session = Depends(get_db), auth_permission: int = Depends(admin_permission)):

    Regex_validation.name_Regex(name=category.category_name)

    # Filter query
    category_query = db.query(models.Category).filter(
        models.Category.id == id, models.Category.is_active == True)

    category_check = category_query.first()

    if category_check == None:
        raise Custom_Validation_Category(
            name=f"Category does not exist.")

    category_query.update(category.dict(), synchronize_session=False)
    db.commit()

    Data = {
        "id": category_check.id,
        "category_name": category_check.category_name,
        "is_active": category_check.is_active,
        "created_at": category_check.created_at
    }

    return {
        "response_code": 200,
        "response_message": "Category have been updated.",
        "response_data": Data
    }


"""
**************
Hard Delete
**************
"""


# Hard Delete
@router.delete(path="/HardDelete/{id}", status_code=status.HTTP_200_OK)
def delete_category(id: int, db: Session = Depends(get_db), auth_permission: int = Depends(admin_permission)):

    category_query = db.query(models.Category).filter(models.Category.id == id)
    category = category_query.first()

    if not category:
        raise Custom_Validation_Category(name="Category does not exist.")

    category_query.delete(synchronize_session=False)
    db.commit()

    return {"response_code": 200,
            "response_message": "Success", }


"""
**************
Soft Delete
**************
"""


@router.delete(path="/SoftDelete/{id}", status_code=status.HTTP_200_OK)
def soft_delete_category(id: int,  db: Session = Depends(get_db), auth_permission: int = Depends(admin_permission)):

    category_query = db.query(models.Category).filter(
        models.Category.id == id, models.Category.is_active == True)
    category_check = category_query.first()

    if not category_check:
        raise Custom_Validation_Category(
            name=f"Category does not exist.")

    category_query.update({"is_active": False}, synchronize_session=False)
    db.commit()

    return {"response_code": 200,
            "response_message": "Success", }


"""
**************
Soft Delete with Relationship 
**************
"""


@router.delete(path="softDeleterelations/{id}", status_code=status.HTTP_200_OK)
def soft_delete_relationship(id: int, db: Session = Depends(get_db), ):

    # Category Query
    category_query = db.query(models.Category).filter(
        models.Category.id == id, models.Category.is_active == True)
    category_check = category_query.first()

    if not category_check:
        raise Custom_Validation_Category(name=" Category does not exist.")

    # Question
    que_query = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.category_id == id, models.ReviewQuestion.is_active == True)
    que_query.update({"is_active": False}, synchronize_session=False)

    db.commit()

    category_query.update({"is_active": False}, synchronize_session=False)
    db.commit()

    return {
        "response_code": 200,
        "response_message": "Success",
    }


@router.get(path="/Search/", status_code=status.HTTP_200_OK, response_model=List[CategorySchemas.OutCategory1])
def search(que: Optional[str] = "", db: Session = Depends(get_db)):
    sss = db.query(models.Category).filter(
        models.Category.re_que.question).all()

    return sss
