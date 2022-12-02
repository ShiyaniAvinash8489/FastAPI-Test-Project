# Date Time
from datetime import datetime
from email.policy import default
from tkinter import CASCADE
from unicodedata import category

# Pydantic
from pydantic import BaseModel

# Database Connection
from app.db_connection import Base

# Import Packages of SQLAlchemy
from sqlalchemy import (Column, Integer, String,
                        Boolean, ForeignKey, DateTime, )

from sqlalchemy_utils import URLType

from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

# For Creating TIMESTAMP in database
from sqlalchemy.sql.sqltypes import TIMESTAMP

# Import Enum for Choice Field
import enum

"""
****************************************************************************************
                                        Models   
****************************************************************************************
"""


"""
************** 
User Model
**************
"""


class User(Base):

    # Set table Name in Postgres Database
    __tablename__ = "User"

    # Column Name and Set fields of Cloumn
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(256), nullable=False, unique=True)
    username = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    phone = Column(String(), nullable=True, unique=True)
    provider = Column(String(), nullable=True, default="email")
    profile_url = Column(String(), nullable=True)

    is_verify = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superadmin = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    review_question = relationship("ReviewQuestion", back_populates="users")
    BLToken = relationship("BlackListToken", back_populates="owner")


"""
************** 
Category 
**************
"""


class Category(Base):

    __tablename__ = "Category"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    category_name = Column(String(100), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    re_que = relationship("ReviewQuestion", back_populates="categ")


"""
************** 
Review Question 
**************
"""


class ReviewQuestion(Base):

    __tablename__ = "ReviewQuestion"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "Category.id", ondelete=CASCADE), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "User.id", ondelete=CASCADE), nullable=False)
    question = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    categ = relationship("Category", back_populates="re_que")
    users = relationship("User", back_populates="review_question")


"""
************** 
Black List Token 
**************
"""


class BlackListToken(Base):

    __tablename__ = "BlackListToken"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey(
        "User.id", ondelete=CASCADE), nullable=False)
    access_token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    owner = relationship("User", back_populates="BLToken")
