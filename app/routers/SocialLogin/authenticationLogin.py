# FastAPI's Modules
from fastapi import Depends

# SQLAlchemy
from sqlalchemy.orm import Session

# Module from application
from app import db_connection, models

# Schemas & oAuth2
from app.routers.authentication import oAuth2

# Hash Password
from app.routers.user import utils


# Validation
from app.routers.authentication import auth


def login(username, password, db: Session = Depends(db_connection.get_db)):

    user = db.query(models.User).filter(
        models.User.email == username).first()

    if not user:
        raise auth.Custom_Validation_Login(name="Invalid Credentials.")

    if not utils.verify(password, user.password):
        raise auth.Custom_Validation_Login(name="Invalid Credentials.")

    if user.is_superadmin or user.is_admin:
        raise auth.Custom_Validation_Login(name="Admin do not Allow")

    if not user.is_verify:
        raise auth.Custom_Validation_Login(
            name="Your account is not verified.")

    if not user.is_active:
        raise auth.Custom_Validation_Login(name="Your account is deleted")

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
