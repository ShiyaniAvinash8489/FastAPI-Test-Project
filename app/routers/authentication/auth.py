# FastAPI Dependency
from fastapi import APIRouter, Depends, status, HTTPException, Response

# FastAPI Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# SQLAlchemy
from sqlalchemy.orm import Session

# Module from application
from app import db_connection, models

# Schemas & oAuth2
from app.routers.authentication import authSchemas, oAuth2

# Hash Password
from app.routers.user import utils

# Confi.py
from app.config import settings

# Twilio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.base import exceptions
from twilio.rest import Client as TwilioClient

# Permission
from app.routers.authentication.oAuth2 import authenticated_permission,  admin_permission


"""
****************************************************************************************
                                    Custom Error Handling
****************************************************************************************
"""


# Custom Error Handling
class Custom_Validation_Login(Exception):
    def __init__(self, name: str):
        self.name = name


"""
****************************************************************************************
                                    Router
****************************************************************************************
"""


# Router - confing in Main.py file
router = APIRouter(prefix="/auth",
                   tags=['Authentication'])


"""
****************************************************************************************
                                    Login API
****************************************************************************************
"""


"""
**************
USER LOGIN
**************
"""


# Login API
@router.post('/login', status_code=status.HTTP_200_OK, response_model=authSchemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connection.get_db)):
    # def login(user_credentials: authSchemas.UserLogin = Depends(), db: Session = Depends(db_connection.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise Custom_Validation_Login(name="Invalid Credentials.")

    if not utils.verify(user_credentials.password, user.password):
        raise Custom_Validation_Login(name="Invalid Credentials.")

    if user.is_superadmin or user.is_admin:
        raise Custom_Validation_Login(name="Admin do not Allow")

    if not user.is_verify:
        raise Custom_Validation_Login(name="Your account is not verified.")

    if not user.is_active:
        raise Custom_Validation_Login(name="Your account is deleted")

    # create a token
    access_token = oAuth2.create_access_token(data={"user_id": user.id})

    data = {
        "userId": user.id,
        "userEmail": user.email,
    }

    # return token
    return {
        "response_code": 200,
        "response_message": "Login Successfully",
        "response_data": data,
        "access_token": access_token,
        "token_type": "bearer"

    }


"""
**************
ADMIN LOGIN
**************
"""


# Admin Login API
@router.post('/admin-login', status_code=status.HTTP_200_OK, response_model=authSchemas.Token)
# def admin_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connection.get_db)):
def login(user_credentials: authSchemas.UserLogin = Depends(), db: Session = Depends(db_connection.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # models.User.email == user_credentials.email).first()

    if not user:
        raise Custom_Validation_Login(name="Invalid Credentials.")

    if not utils.verify(user_credentials.password, user.password):
        raise Custom_Validation_Login(name="Invalid Credentials.")
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not user.is_superadmin or not user.is_admin:
        raise Custom_Validation_Login(name="Only Admin Allow")

    if not user.is_verify:
        raise Custom_Validation_Login(name="Your account is not verified.")

    if not user.is_active:
        raise Custom_Validation_Login(name="Your account is deleted")

    # create a token
    access_token = oAuth2.create_access_token(data={"user_id": user.id})

    data = {
        "user_id": user.id,
        "user_email": user.email,
    }

    # return token
    return {
        "response_code": 200,
        "response_message": "Login Successfully",
        "response_data": data,
        "access_token": access_token,
        "token_type": "bearer"

    }


"""
****************************************************************************************
                        Login API with Two factor Authentication
****************************************************************************************
"""


"""
**************
Twilio Settings
**************
"""


# Twilio Code
client = Client(settings.twilio_sid, settings.twilio_auth_token)
verify = client.verify.services(settings.twilio_service_id)


"""
**************
USER LOGIN Two factore
**************
"""


# Login API
@router.post('/Two-factore-Login', status_code=status.HTTP_200_OK, response_model=authSchemas.Token_otp)
def login(user_credentials: authSchemas.UserLogin = Depends(), db: Session = Depends(db_connection.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise Custom_Validation_Login(name="Invalid Credentials.")

    if not utils.verify(user_credentials.password, user.password):
        raise Custom_Validation_Login(name="Invalid Credentials.")
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if user.is_superadmin or user.is_admin:
        raise Custom_Validation_Login(name="Admin do not Allow")

    if not user.is_verify:
        raise Custom_Validation_Login(name="Your account is not verified.")

    if not user.is_active:
        raise Custom_Validation_Login(name="Your account is deleted")

    # Send OTP
    verify.verifications.create(to=user.phone, channel='sms')

    data = {
        "user_phone": user.phone,
        "username": user.email,
    }

    # return token
    return {
        "response_code": 200,
        "response_message": "Opt have been sent",
        "response_data": data,
    }


"""
**************
Verify OTP
**************
"""


@router.post('/verify_otp', status_code=status.HTTP_200_OK, response_model=authSchemas.Token,)
def verify_otp(userotp: authSchemas.VerifyOTP, db: Session = Depends(db_connection.get_db)):
    # def login(user_credentials: schemas.UserLogin = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.phone == userotp.phone).first()

    try:
        result = verify.verification_checks.create(
            to=userotp.phone, code=userotp.otp)
        if result.status == "approved":
            # create a token
            access_token = oAuth2.create_access_token(
                data={"user_id": user.id})

            data = {
                "userId": user.id,
                "userEmail": user.email,
            }

            # return token
            return {
                "response_code": 200,
                "response_message": "Login Successfully",
                "response_data": data,
                "access_token": access_token,
                "token_type": "bearer"

            }

        if result.status == "pending":
            raise Custom_Validation_Login(
                name="You have entered incorrect OTP, Please Enter Correct OTP.")

        if result.status == "expired":
            raise Custom_Validation_Login(
                name="Your OTP is Expired. Please Resend OTP.")

    except TwilioRestException:
        print('no')
        raise Custom_Validation_Login(
            name=TwilioRestException)


"""
**************
Black List Token
**************
"""


@router.post(path="/logout", status_code=status.HTTP_200_OK)
def blacklist_token(token: authSchemas.BlackListToken, db: Session = Depends(db_connection.get_db),
                    current_user: int = Depends(authenticated_permission)):

    bl_token = models.BlackListToken(user_id=current_user.id,
                                     access_token=token.token

                                     )

    db.add(bl_token)
    db.commit()
    db.refresh(bl_token)

    return {
        "response_code": 200,
        "response_message": "Successfully Logout",
    }
