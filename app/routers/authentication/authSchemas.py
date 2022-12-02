# Pydantic
from pydantic import BaseModel, EmailStr, Field

from typing import Optional


"""
****************************************************************************************
                            Login   &  Two Factore Authentication - OTP
****************************************************************************************
"""


"""
************** 
User Login
**************
"""


# User Login
class UserLogin(BaseModel):
    Email: EmailStr
    Password: str


"""
************** 
Verify OTP
**************
"""


# User Login
class VerifyOTP(BaseModel):
    phone: str
    otp: str


# Token After verifing OTP
class Token_otp(BaseModel):
    response_code: int
    response_message: str
    response_data: dict


"""
****************************************************************************************
                            JWT Authencication - Schemas   
****************************************************************************************
"""


# Authenication Shcema base on in auth.py
class Token(BaseModel):
    response_code: int
    response_message: str
    response_data: dict
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


"""
************** 
Black List Token 
**************
"""


class BlackListToken(BaseModel):

    token: str
