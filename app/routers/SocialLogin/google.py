# Google
from google.auth.transport import requests
from google.oauth2 import id_token

# Confings
from app.config import settings

# Import Modules
from app import models

# Hash Key
from app.routers.user import utils

# SQlAlchemy ORM
from sqlalchemy.orm import Session
from fastapi import Depends

# Import database Settings
from app.db_connection import get_db

# random
import random

# Login API
from app.routers.SocialLogin import authenticationLogin

# Create Token
from app.routers.authentication import oAuth2

# Validations
from app.routers.authentication.auth import Custom_Validation_Login

"""
****************************************************************************************
                                    Google 
****************************************************************************************
"""


"""
**************
Google Logic
**************
"""


class Google:

    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return {
                "response_code": 400,
                "response_message": "The token is invalid or expired. Please login again."
            }


"""
****************************************************************************************
                    Store Social login data in User Model
****************************************************************************************
"""


"""
**************
Create Username
**************
"""


def generate_username(name, db):

    username = "".join(name.split(' ')).lower()
    if not db.query(models.User).filter(models.User.username == name).first():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


"""
**************
Get Access Token after Social Login 
**************
"""


def Create_User_For_Login_token(email, name, provider, db: Session = Depends(get_db)):

    # Check to exists email or not in User Model
    filtered_user_by_email = db.query(models.User).filter(
        models.User.email == email).first()

    if filtered_user_by_email:

        if provider == filtered_user_by_email.provider:

            return authenticationLogin.login(
                username=email, password=settings.google_password, db=db)

        else:

            return Custom_Validation_Login(name=f"Please continue your login using  {filtered_user_by_email[0].auth_provider}")

    else:

        # Save Social Login Details in User Models
        user = models.User(
            username=generate_username(name, db=db),
            email=email,
            password=utils.hash("settings.google_password"),
            is_verify=True,
            provider=provider,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Create Token
        data = {
            "user_id": user.id,
            "user_email": email
        }

        # Generete Access Token after saving data into User models
        UserToken = oAuth2.create_access_token(data=data)

        return {
            "response_code": 200,
            "response_message": "Login Successfully",
            "response_data": data,
            "access_token": UserToken,
            "token_type": "bearer"
        }
