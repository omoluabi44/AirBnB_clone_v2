#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import models
from models.place import Place
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    __tablename__ = "users"
    """This class defines a user by various attributes"""
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship("Place",
                          cascade='all, delete, delete-orphan', backref="user")
    reviews = relationship("Review",
                           cascade='all, delete, delete-orphan',
                           backref="user")
