# Settings
from app.config import settings

# Import JWT Token
from jose import JWTError, jwt
from jose import ExpiredSignatureError

# Import Datetime for expiring Token
from datetime import datetime, timedelta

# Import Models and db_connection
from app import models, db_connection

# Schemas
from app.routers.authentication import authSchemas

# FastAPI Dependency
from fastapi import Depends
from sqlalchemy.orm import Session

# FastAPI Security
from fastapi.security import OAuth2PasswordBearer


"""
****************************************************************************************
                                    Setting of JWT
****************************************************************************************
"""

# Reverse Login api
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


"""
**************
Authenticated Permission / Token  - Custom Error Handling
**************
"""


class Custom_Validation_Oauth2(Exception):
    def __init__(self, name: str):
        self.name = name


"""
****************************************************************************************
                            Create JWT and Verify Token
****************************************************************************************
"""


"""
**************
Create Access Token
**************
"""


# Create Access Token
def create_access_token(data: dict):
    to_encode = data.copy()

    # expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    print("\n\n\n\n\n")
    print(to_encode)
    print("\n\n\n\n\n")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


"""
**************
Verify Token
**************
"""

# Verify Access Token


# def verify_access_token(token: str, credentials_exception):
def verify_access_token(token: str):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise Custom_Validation_Oauth2(name="Invalid Token")
        token_data = authSchemas.TokenData(id=id)

    except ExpiredSignatureError:

        raise Custom_Validation_Oauth2(name="Token is expired")

    except JWTError:
        raise Custom_Validation_Oauth2(name="Invalid Token")
    return token_data


"""
****************************************************************************************
                            Authentication Permission
****************************************************************************************
"""


"""
**************
Authenticated Permission
**************
"""


# Authentication Permission
def authenticated_permission(token: str = Depends(oauth2_scheme),
                             db: Session = Depends(db_connection.get_db)):

    credentials_exception = Custom_Validation_Oauth2(name=" Unauthorized ")

    # Getting Boolean return
    # return verify_access_token(token, credentials_exception)

    token = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    if user:
        return user
    else:
        raise credentials_exception


"""
**************
Admin Permission
**************
"""


# Admin Permission
def admin_permission(token: str = Depends(oauth2_scheme), db: Session = Depends(db_connection.get_db)):
    credentials_exception = Custom_Validation_Oauth2(name=" Unauthorized ")

    token = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    # if user.is_superadmin and user.is_admin:
    if user.is_superadmin or user.is_admin:
        return user
    else:
        raise credentials_exception
