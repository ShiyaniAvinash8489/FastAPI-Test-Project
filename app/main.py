# FastAPI Instance
from fastapi import (FastAPI,
                     Request,
                     responses,
                     )
# Status
from fastapi import status

# MiddleWare
from fastapi.middleware.cors import CORSMiddleware

# Static File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Setting - Config
from app.config import settings

# Model
from app import models

# DataBase Engine
from app.db_connection import engine

# Validation
from app.routers.user.validation import Custom_Validation
from app.routers.authentication.auth import Custom_Validation_Login
from app.routers.authentication.oAuth2 import Custom_Validation_Oauth2
from app.routers.user.userRouter import Custom_Validation_User
from app.routers.category.CategoryRouter import Custom_Validation_Category

# Router
from app.routers.user import userRouter
from app.routers.authentication import auth
from app.routers.category import CategoryRouter
from app.routers.Review import ReviewRouter
from app.routers.CSV import csvRouter
from app.routers.SocialLogin import SocialRouter
"""
****************************************************************************************
                    Database Connection, Instance  
****************************************************************************************
"""

# Instance with Swagger Settings
app = FastAPI(
    title="Advance FastAPI",
    description="Basic Structure",
    version="0.0.1",
    terms_of_service="https://fastapi.tiangolo.com/tutorial/metadata/",
    contact={
        "name": "FastAPI",
            "userl": "https://fastapi.tiangolo.com/tutorial/metadata/",
            "email": "ks4223839@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/swagger"
)


models.Base.metadata.create_all(bind=engine)


"""
****************************************************************************************
                                CORS Headers & Middleware 
****************************************************************************************
"""
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
****************************************************************************************
                                        Router  
****************************************************************************************
"""

app.include_router(userRouter.router)
app.include_router(auth.router)
app.include_router(CategoryRouter.router)
app.include_router(ReviewRouter.router)
app.include_router(csvRouter.router)
app.include_router(SocialRouter.router)


"""
****************************************************************************************
                    Static File & Templates  & Default Link
****************************************************************************************
"""

"""
************** 
Static File
**************
"""
app.mount("/static", StaticFiles(directory="static"), name="static")


"""
************** 
Template
**************
"""
templates = Jinja2Templates(directory="templates")


"""
************** 
Default Link
**************
"""


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}


"""
****************************************************************************************
                                   Custom Validation & Error Handling 
****************************************************************************************
"""


# For Validation.py
@app.exception_handler(Custom_Validation)
async def unicorn_exception_handler_validation(request: Request, exc: Custom_Validation):
    return responses.JSONResponse(
        status_code=400,
        content={
            "response_code": 400,
            "response_message": f" {exc.name}"},
    )


# For Login in routers/auth.py
@app.exception_handler(Custom_Validation_Login)
async def unicorn_exception_handler_login(request: Request, exc: Custom_Validation_Login):
    return responses.JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "response_code": 401,
            "response_message": f" {exc.name}"},
    )


# For Data Not Found - user.py
@app.exception_handler(Custom_Validation_User)
async def unicorn_exception_handler_404(request: Request, exc: Custom_Validation_User):
    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "response_code": 404,
            "response_message": f"{exc.name}"
        }
    )


# For Authentication Permisison /Token - oauth2.py
@app.exception_handler(Custom_Validation_Oauth2)
async def unicorn_exception_handler_permission(request: Request, exc: Custom_Validation_Oauth2):
    return responses.JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "response_code": 401,
            "response_message": f"{exc.name}"
        },
        headers={"WWW-Authenticate": "Bearer"}
    )


# For Category
@app.exception_handler(Custom_Validation_Category)
async def unicorn_exception_handler_validation(request: Request, exc: Custom_Validation_Category):
    return responses.JSONResponse(
        status_code=400,
        content={
            "response_code": 400,
            "response_message": f" {exc.name}"},
    )
