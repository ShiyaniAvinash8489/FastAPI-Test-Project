# Import Session
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

# Import Models
from app import models

# Validation
from app.routers.category.CategoryRouter import Custom_Validation_Category

"""
****************************************************************************************
                                    Custom Error Handling 
****************************************************************************************
"""


class Custom_Validation(Exception):
    def __init__(self, name: str):
        self.name = name


"""
****************************************************************************************
                                    Custom Validation  
****************************************************************************************
"""


def User_exist(db: Session, id: int):
    if not db.query(models.User).filter(
            models.User.id == id, models.User.is_active == True).first():
        raise Custom_Validation_Category(name="User doesn't exist.")


def category_exist(db: Session, id: int):
    if not db.query(models.Category).filter(
            models.Category.id == id, models.Category.is_active == True).first():
        raise Custom_Validation_Category(name="Category does't exist")
