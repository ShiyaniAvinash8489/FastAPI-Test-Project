# Packages of FastAPI
from fastapi import (status,
                     Depends,
                     APIRouter,
                     Request,
                     templating,
                     responses,
                     UploadFile,
                     File,
                     )

from pydantic import EmailStr
from requests import request

# SQlAlchemy ORM
from sqlalchemy.orm import Session

# Import Modules
from app import models

# Import database Settings
from app.db_connection import get_db

# Validation
from app.routers.user import validation, utils, userSchemas
from app import Regex_validation

# Permission For API
from app.routers.authentication.oAuth2 import authenticated_permission,  admin_permission

# typing
from typing import List

# Email
from app.email.emailConfig import send_email_verify_account_html

# Token
from app.routers.authentication.oAuth2 import create_access_token, verify_access_token

# Password
from app.routers.user import utils

# shutil for image
import shutil

"""
****************************************************************************************
                                    Router Setting
****************************************************************************************
"""


# Routers Settings
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


"""
****************************************************************************************
                                    Custom Error Handling
****************************************************************************************
"""


# Custom Error Handling
class Custom_Validation_User(Exception):
    def __init__(self, name: str):
        self.name = name


"""
****************************************************************************************
                                    Create User
****************************************************************************************
"""


"""
**************
CREATE USER
**************
"""


# Create Normal User
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: userSchemas.UserCreate, db: Session = Depends(get_db), ):

    # Email Exist Validation
    validation.email_exist(db=db, email=user.email)

    # Username Exist Validation & Regex Validation
    Regex_validation.username_Regex(username=user.username)
    validation.username_exist(db=db, username=user.username)

    # Phone Exist Validation & Regex Validation
    Regex_validation.phone_regex(phone=user.phone)
    validation.phone_exist(db=db, phone=user.phone)

    # # Email - Validation With Regex
    # validation.email_Regex(db=db, email=user.email)

    # Name Validation
    Regex_validation.name_Regex(name=user.first_name)
    Regex_validation.name_Regex(name=user.last_name)

    # hash the password - user.password
    Regex_validation.password_regex(password=user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Save User Data in Models User
    new_user = models.User(**user.dict(), )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create Token
    data = {
        "user_id": new_user.id,
    }

    # For Testing Purpose
    user_query = db.query(models.User).filter(models.User.id == new_user.id)
    user_check = user_query.first()

    user_query.update({"is_verify": True},
                      synchronize_session=False)

    db.commit()

    UserToken = create_access_token(data=data)

    # Email Body
    email_body = f"Please verify your account \n http://localhost:8000/users/verifyAccount/?token={UserToken} "

    # Email
    send_email_verify_account_html(
        To=user.email, Subject="Verify Account", email_body=email_body)

    UserData = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "username": new_user.username,
        "phone": new_user.phone,
        "profile_url": new_user.profile_url
    }

    # return new_user
    return {
        "response_code": 201,
        "response_message": "Account have been created. Email have been sent on your Register email address",
        "response_data": UserData,
    }


"""
**************
Verify Account
**************
"""


@router.get("/verifyAccount", status_code=status.HTTP_201_CREATED)
async def email_verification(request: Request, token: str,  db: Session = Depends(get_db)):

    # Verify Token
    UserData = verify_access_token(token=token)

    user_query = db.query(models.User).filter(models.User.id == UserData.id)
    user_check = user_query.first()

    user_query.update({"is_verify": True},
                      synchronize_session=False)

    db.commit()

    return {
        "response_code": 200,
        "response_message": "Your account have been verified. Now You can Login.",
    }


"""
**************
Create Admin User
**************
"""


# Create Admin User
@router.patch("/create-admin/{email}", status_code=status.HTTP_201_CREATED)
def create_super_user(email: EmailStr,  db: Session = Depends(get_db), current_user: int = Depends(admin_permission)):

    # Filter query
    user_query = db.query(models.User).filter(models.User.email == email)
    user_check = user_query.first()

    if user_check == None:
        raise Custom_Validation_User(
            name=f"post with id: '{email}' does not exist")

    user_query.update({"is_superadmin": True, "is_admin": True},
                      synchronize_session=False)
    db.commit()

    # return user_query.first()
    return {
        "response_code": 201,
        "response_message": f"Now, {email} is admin.",
    }


"""
**************
Update Specific User
**************
"""


# Create Update
@router.patch("/Update", status_code=status.HTTP_201_CREATED, )
def Update_User(user: userSchemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(authenticated_permission)):

    # Name Validation
    Regex_validation.name_Regex(name=user.first_name)
    Regex_validation.name_Regex(name=user.last_name)

    # Filter query
    user_query = db.query(models.User).filter(
        models.User.id == current_user.id)
    user_check = user_query.first()

    if user_check == None:
        raise Custom_Validation_User(
            name=f"post with id: '{current_user}' does not exist")

    if not user.first_name:
        user.first_name = current_user.first_name
    elif not user.last_name:
        user.last_name = current_user.last_name

    if not user.email:
        user.email = current_user.email
    else:
        validation.email_exist(db=db, email=user.email)

    if not user.username:
        user.username = current_user.username
    else:
        Regex_validation.username_Regex(username=user.username)
        validation.username_exist(db=db, username=user.username)

    if not user.phone:
        user.phone = current_user.phone
    else:
        validation.phone_exist(db=db, phone=user.phone)
        Regex_validation.phone_regex(phone=user.phone)

    user_query.update(user.dict(), synchronize_session=False)
    db.commit()

    UserData = {
        "id": current_user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
        "phone": user.phone,
    }
    # return user_query.first()
    return {
        "response_code": 201,
        "response_message": "Data have been updated",
        "response_data": UserData

    }


"""
**************
Get Specific User
**************
"""


# Get specific User
@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(admin_permission)):
    # def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise Custom_Validation_User(name=f"User with id: {id} does not exist")

    UserData = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,

    }

    return {
        "response_code": 200,
        "response_message": "Success",
        "response_data": UserData
    }


"""
**************
Get All User
**************
"""


@router.get(path="/get_all", status_code=status.HTTP_200_OK, response_model=List[userSchemas.UserOut])
def get_all_user(database: Session = Depends(get_db), current_user: int = Depends(admin_permission)):

    user = database.query(models.User).filter(
        models.User.is_verify == True, models.User.is_active == True).all()

    return user


"""
**************
Hard Delete 
**************
"""


@router.delete(path="/HardDelete/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(admin_permission)):

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise Custom_Validation_User(name="User does not exist.")

    user_query.delete(synchronize_session=False)
    db.commit()

    return {"response_code": 200,
            "response_message": "Success", }


"""
**************
Soft Delete
**************
"""


@router.delete(path="/SoftDelete/{id}", status_code=status.HTTP_200_OK)
def soft_delete_user(id: int, db: Session = Depends(get_db), auth_permission: int = Depends(admin_permission)):

    user_query = db.query(models.User).filter(
        models.User.id == id, models.User.is_active == True)
    user_check = user_query.first()

    if not user_check:
        raise Custom_Validation_User(name="User does not exist.")

    user_query.update({"is_active": False}, synchronize_session=False)
    db.commit()

    return {"response_code": 200,
            "response_message": "Success", }


"""
**************
Update/ Change Password 
**************
"""


# Change Password
@router.patch("/Change-Password", status_code=status.HTTP_200_OK)
def change_password(user: userSchemas.UpdatePassword, db: Session = Depends(get_db),
                    current_user: int = Depends(authenticated_permission)):

    user_query = db.query(models.User).filter(
        models.User.id == current_user.id)
    user_check = user_query.first()

    if not user_check:
        raise Custom_Validation_User(
            name=f"post with id: '{current_user}' does not exist")

    if not utils.verify(user.oldPassword, user_check.password):

        raise Custom_Validation_User(name="Old password does not match.")

    Regex_validation.password_regex(password=user.newPassword)

    hash_password = utils.hash(user.newPassword)
    user_query.update({"password": hash_password}, synchronize_session=False)
    db.commit()

    return {
        "response_code": 201,
        "response_message": "Password have been changed.",
    }


"""
**************
Update/ Change Password 
**************
"""


@router.post("/create_user_image", status_code=status.HTTP_201_CREATED)
def create_user(first_name: str, last_name: str, email: str, username: str, phone: str, password: str, profile_ulr: UploadFile = File(...), db: Session = Depends(get_db), ):

    # Email Exist Validation
    validation.email_exist(db=db, email=email)

    # Username Exist Validation & Regex Validation
    Regex_validation.username_Regex(username=username)
    validation.username_exist(db=db, username=username)

    # Phone Exist Validation & Regex Validation
    Regex_validation.phone_regex(phone=phone)
    validation.phone_exist(db=db, phone=phone)

    # # Email - Validation With Regex
    # validation.email_Regex(db=db, email=user.email)

    # Name Validation
    Regex_validation.name_Regex(name=first_name)
    Regex_validation.name_Regex(name=last_name)

    # hash the password - user.password
    Regex_validation.password_regex(password=password)
    hashed_password = utils.hash(password)
    password = hashed_password

    # File Store
    file_location = f"static/UserProfile/{profile_ulr.filename}"
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(profile_ulr.file, file_object)

    # Save User Data in Models User
    new_user = models.User(first_name=first_name, last_name=last_name, password=password,
                           email=email, username=username, profile_url=str(file_location), phone=phone)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create Token
    data = {
        "user_id": new_user.id,
    }

    UserToken = create_access_token(data=data)

    # Email Body
    email_body = f"Please verify your account \n http://localhost:8000/users/verifyAccount/?token={UserToken} "

    # # Email
    # send_email_verify_account_html(
    #     To=user.email, Subject="Verify Account", email_body=email_body)

    UserData = {
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "username": new_user.username,
        "phone": new_user.phone,
        "profile_url": new_user.profile_url
    }

    # return new_user
    return {
        "response_code": 201,
        "response_message": "Account have been created. Email have been sent on your Register email address",
        "response_data": UserData,
    }
