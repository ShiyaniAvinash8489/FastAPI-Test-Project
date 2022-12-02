# Import Session
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

# Import Models
from app import models

# Regex
import re

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

# Exist Email Validations


def email_exist(db: Session, email: str):
    if db.query(models.User).filter(models.User.email == email).first():
        raise Custom_Validation(name="Email already registered ")


# Exist Username Validations
def username_exist(db: Session, username: str):
    if db.query(models.User).filter(models.User.username == username).first():
        raise Custom_Validation(name="Username already registered")


# Exist Phone Validations
def phone_exist(db: Session, phone: str):
    if db.query(models.User).filter(models.User.phone == phone).first():
        raise Custom_Validation(name="Phone already registered")


# Email Validation
def email_Regex(db: Session, email: str):
    if not re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", email):
        raise Custom_Validation(name="Invalid Email")


"""
****************************************************************************************
                            HTTPException Error handling  
****************************************************************************************
"""
# def email_exist(db: Session, email: str):
#     if db.query(models.User).filter(models.User.email == email).first():
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail={
#                 "ResponseCode": 400,
#                 "ResponseMsg": "Email already registered"
#             },
#         )
