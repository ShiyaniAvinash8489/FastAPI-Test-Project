from fastapi import (status,
                     Depends,
                     APIRouter,
                     responses,
                     Request
                     )


# SQLAlchmey ORM
from sqlalchemy.orm import Session


# Import database Settings
from app.db_connection import get_db


# Conging
from app.config import settings

# template
from app import main


# Schemas
from app.routers.SocialLogin import SocialSchemas


# Google
from app.routers.SocialLogin.google import Google, Create_User_For_Login_token


"""
****************************************************************************************
                                    Router Setting
****************************************************************************************
"""


# Routers Settings
router = APIRouter(
    prefix="/Social",
    tags=['Social']
)


"""
****************************************************************************************
                                    Social Login
****************************************************************************************
"""


"""
**************
Google Templates 
**************
"""


# Google Login with template for getting access token from google.
@router.get("/GoogleTemplate", response_class=responses.HTMLResponse)
def google_index(request: Request):
    context = {"request": request}
    return main.templates.TemplateResponse("google.html", context)


"""
**************
Google Login
**************
"""


@router.post("/GoogleToken", status_code=status.HTTP_200_OK)
def googleLogin(token: SocialSchemas.GoogleSchema, db: Session = Depends(get_db)):

    user_data = Google.validate(auth_token=token.token)

    try:
        user_data["sub"]
    except:
        return {
            "response_code": 400,
            "response_message": "The token is invalid or expired. Please login again."
        }

    if user_data['aud'] != (settings.google_client_id):
        return {
            "response_code": 400,
            "response_message": "You are not Login with diffrent google Client Id."
        }

    user_id = user_data['sub']
    email = user_data['email']
    name = user_data['name']
    provider = 'google'

    return Create_User_For_Login_token(email=email, name=name, provider=provider, db=db)
