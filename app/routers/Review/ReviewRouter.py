from fastapi import (status,
                     Depends,
                     APIRouter,
                     )

from pydantic import EmailStr
from requests import request
from sqlalchemy import true

# SQLAlchmey ORM
from sqlalchemy.orm import Session

# Import Modules
from app import models

# Import database Settings
from app.db_connection import get_db
from app import db_connection

# Schemas
from app.routers.Review import ReviewSchemas

# Permission for API
from app.routers.authentication.oAuth2 import authenticated_permission, admin_permission

# Typing
from typing import List, Optional


# Custom Validation
from app.routers.category.CategoryRouter import Custom_Validation_Category
from app.routers.Review import ReviewValidation


"""
****************************************************************************************
                                    Router Setting
****************************************************************************************
"""


# Routers Settings
router = APIRouter(
    prefix="/Review",
    tags=['Review']
)


"""
****************************************************************************************
                                    CRUD  Question
****************************************************************************************
"""

# , auth_permission: int = Depends(admin_permission)
"""
**************
Create
**************
"""


# Create Category with Regex validation
@router.post("/create-Question", status_code=status.HTTP_201_CREATED)
def create_Question(ReQue: ReviewSchemas.ReviewQuestion, db: Session = Depends(get_db)):

    ReviewValidation.category_exist(db=db, id=ReQue.category_id)
    ReviewValidation.User_exist(db=db, id=ReQue.user_id)

    ReviewQue = models.ReviewQuestion(**ReQue.dict())

    db.add(ReviewQue)
    db.commit()
    db.refresh(ReviewQue)

    Data = {
        "id": ReviewQue.id,
        "category_id": ReviewQue.category_id,
        "category_name": ReviewQue.categ.category_name,
        "user_id": ReviewQue.user_id,
        "user_name": ReviewQue.users.first_name,
        "question": ReviewQue.question,
        "is_active": ReviewQue.is_active,
        "created_at": ReviewQue.created_at
    }

    # return new_user
    return {
        "response_code": 201,
        "response_message": "Review Question have been created.",
        "response_data": Data,
    }


"""
**************
Get All
**************
"""


#

# # Get All Question with Relationship
# @router.get(path="/get_all_relationship", status_code=status.HTTP_200_OK, response_model=List[ReviewSchemas.OutReviewQuestionWithRelationship])
# def get_all_relationship(database: Session = Depends(get_db)):

#     que_query = database.query(models.ReviewQuestion).filter(
#         models.ReviewQuestion.is_active == True).all()

#     return que_query


"""
**************
Get single
**************
"""


# Get Specific Question
@router.get(path="/{id}", status_code=status.HTTP_200_OK)
def get_question(id: int, db: Session = Depends(get_db),):

    question_query = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.id == id, models.ReviewQuestion.is_active == True).first()

    if not question_query:
        raise Custom_Validation_Category(name="Question does not exist.")

    Data = {
        "id": question_query.id,
        "category_id": question_query.category_id,
        "category_name": question_query.categ.category_name,
        "user_id": question_query.user_id,
        "user_name": question_query.users.first_name,
        "question": question_query.question,
        "is_active": question_query.is_active,
        "created_at": question_query.created_at
    }

    return {
        "response_code": 200,
        "response_message": "Success",
        "response_data": Data
    }


# RelationsShip
@router.get(path="/relationship/{id}", status_code=status.HTTP_200_OK)
def get_question_relationalship(id: int, db: Session = Depends(get_db),):

    question_query = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.id == id, models.ReviewQuestion.is_active == True).first()

    if not question_query:
        raise Custom_Validation_Category(name="Question does not exist.")

    Data = {
        "id": question_query.id,
        "category_id": question_query.category_id,
        "category_name": question_query.categ.category_name,
        "user_id": question_query.user_id,
        "user_name": question_query.users.first_name,
        "question": question_query.question,
        "is_active": question_query.is_active,
        "created_at": question_query.created_at,
        "Link_Data": {"category": question_query.categ,
                      "user": question_query.users
                      }
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
def Update_Question(id: int, ReQue: ReviewSchemas.ReviewQuestionUpdate, db: Session = Depends(get_db)):

    # Filter query
    question_query = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.id == id, models.ReviewQuestion.is_active == True)

    question_check = question_query.first()

    if question_check == None:
        raise Custom_Validation_Category(
            name=f"Question does not exist.")

    if not ReQue.category_id:
        ReQue.category_id = question_check.category_id
    else:
        ReviewValidation.category_exist(db=db, id=ReQue.category_id)
    if not ReQue.user_id:
        ReQue.user_id = question_check.user_id
    else:
        ReviewValidation.User_exist(db=db, id=ReQue.user_id)

    question_query.update(ReQue.dict(), synchronize_session=False)
    db.commit()

    Data = {
        "id": question_check.id,
        "category_id": question_check.category_id,
        "category_name": question_check.categ.category_name,
        "user_id": question_check.user_id,
        "user_name": question_check.users.first_name,
        "question": question_check.question,
        "is_active": question_check.is_active,
        "created_at": question_check.created_at,
    }

    return {
        "response_code": 200,
        "response_message": "Question have been updated.",
        "response_data": Data
    }


"""
**************
Hard Delete
**************
"""


# Hard Delete
@ router.delete(path="/HardDelete/{id}", status_code=status.HTTP_200_OK)
def delete_question(id: int, db: Session = Depends(get_db)):

    question_query = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.id == id)
    question = question_query.first()

    if not question:
        raise Custom_Validation_Category(name="Question does not exist.")

    question_query.delete(synchronize_session=False)
    db.commit()

    return {"response_code": 200,
            "response_message": "Success", }


"""
**************
Soft Delete
**************
"""


@ router.delete(path="/SoftDelete/{id}", status_code=status.HTTP_200_OK)
def soft_delete_question(id: int,  db: Session = Depends(get_db),):

    question_query = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.id == id, models.ReviewQuestion.is_active == True)
    question = question_query.first()

    if not question:
        raise Custom_Validation_Category(
            name=f"Question does not exist.")

    question_query.update({"is_active": False}, synchronize_session=False)
    db.commit()

    return {"response_code": 200,
            "response_message": "Success", }


"""
**************
Create Question with Category 
**************
"""


@router.post("/Cat-Que", status_code=status.HTTP_201_CREATED)
def createCatQue(cq: ReviewSchemas.CreateCateQue, db: Session = Depends(get_db)):

    category = models.Category(**cq.category.dict())
    db.add(category)
    db.commit()
    db.refresh(category)

    question = models.ReviewQuestion(
        category_id=category.id, **cq.question.dict())
    db.add(question)
    db.commit()
    db.refresh(question)

    Data = {
        "id": category.id,
        "category_name": category.category_name,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "Question": category.re_que
    }

    return {
        "response_code": 201,
        "response_message": "Data is Created",
        "response_data": Data
    }


"""
**************
RND
**************
"""


@router.get(path="/Search/", status_code=status.HTTP_200_OK, response_model=List[ReviewSchemas.OutReviewQuestion])
def search(que: Optional[str] = "", db: Session = Depends(get_db)):
    sss = db.query(models.ReviewQuestion, models.Category).filter(
        models.ReviewQuestion.question.contains(que)).all()

    return sss


@router.get(path="/QueryRND/", status_code=status.HTTP_200_OK)
def searchRND(que: Optional[int] = "", db: Session = Depends(get_db)):

    # # Count
    # CountQuery = db.query(models.ReviewQuestion).filter(
    #     models.ReviewQuestion.question.contains(que)).count()

    # CountQuery = {"Count": CountQuery}

    # Count
    CountQuery = db.query(models.ReviewQuestion).filter(
        models.ReviewQuestion.question).all()

    CountQuery = {"Count": CountQuery}
    return CountQuery
