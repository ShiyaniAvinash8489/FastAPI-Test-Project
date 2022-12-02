# Password
from passlib.context import CryptContext


"""
****************************************************************************************
                                    Hash Key Password
****************************************************************************************
"""

# Set Hash Content
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
************** 
Create Hash Key Password  
**************
"""


def hash(password: str):
    return pwd_context.hash(password)


"""
************** 
Verify Hash Key Password  
**************
"""


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
