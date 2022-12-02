# Import Session
from sqlalchemy.orm import Session

# Import Models
from app import models

# Regex
import re

# Custom Validation
from app.routers.user.validation import Custom_Validation

"""
****************************************************************************************
                                    Custom Error Handling 
****************************************************************************************
"""


"""
****************************************************************************************
                                    Regex Validation  
****************************************************************************************
"""


# Email Validation
def email_Regex(db: Session, email: str):
    if not re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", email):
        raise Custom_Validation(name="Invalid Email")


# Name Validaiton
def name_Regex(name: str):
    if not re.match("^[a-zA-Z][a-zA-Z\s]*[a-zA-Z]$", name):
        raise Custom_Validation(
            name=f" '{name}' must been allow alphabet and White Space.")


# Username
def username_Regex(username: str):
    if not re.match("^[a-zA-Z0-9].[a-zA-Z0-9\.\-_]*[a-zA-Z0-9]$", username):
        raise Custom_Validation(name="Username is not allow.")


# Phone
def phone_regex(phone: str):
    if not re.match("^[+][0-9]*$", phone):
        raise Custom_Validation(name=f" phone is not allow.")
    if len(phone) < 13 or len(phone) > 15:
        raise Custom_Validation(name="Phone's Length should be 12 to 15 ")


# Password
def password_regex(password: str):
    if not re.search(re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"), password):
        raise Custom_Validation(name=f" password is not allow.")


#  1. Should have at least one number.
# 2. Should have at least one uppercase and one lowercase character.
# 3. Should have at least one special symbol.
# 4. Should be between 6 to 20 characters long."""
