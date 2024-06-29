#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Database storage engine for MySQL"""
    __engine = None
    __session = None

    def __init__(self):
        usr = getenv('HBNB_MYSQL_USER')
        usrpsw = getenv('HBNB_MYSQL_PWD')
        usrhst = getenv('HBNB_MYSQL_HOST')
        usrdb = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(usr, usrpsw, usrhst, usrdb),
                                      pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """All the object in the current database session"""
        result = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = []
            for model_class in [User, State, City, Amenity, Place, Review]:
                objects.extend(self.__session.query(model_class).all())
        for obj in objects:
            key = f"{type(obj).__name__}.{obj.id}"
            result[key] = obj

        return result

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """save the object to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize session with the database"""
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()
