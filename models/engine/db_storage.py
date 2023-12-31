#!/usr/bin/python3
"""
database storage using mysql
It imports modules from the respective directories
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.review import Review
from models.state import State
from models.place import Place

"""
The code defines a dictionary classes that
maps class names to actual class objects
"""
classes = {"User": User, "State": State, "City": City, "Amenity": Amenity,
           "Place": Place, "Review": Review}


class DBStorage:
    """private class attributes __engine and __session"""

    __engine = None
    __session = None

    def __init__(self):
        """instantiate class DBStorage object.
        It retrieves necessary environment variables
        for connecting to the database"""
        HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")
        HBNB_ENV = os.getenv("HBNB_ENV")

        """
        Creates a SQLAlchemy engine using the create_engine function
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        """If environment is set to test,
        it drops all tables in the database"""
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """queries the current database session
        for all objects of a given class if cls is not specifies"""
        obj_dict = {}
        classes = [User, State, City, Place, Review]

        if cls:
            classes = [cls]
        for cls in classes:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """add an object to a db session and raises and exception if there's an error"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as err:
                self.__session.rollback()
                raise err

    def save(self):
        """commit changes to db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from db session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database using the SQLAlchemy metadata
        and setsup sessionmaker with the engine. It assigns the session to the private __session attributes"""
        Base.metadata.create_all(self.__engine)
        Base.metadata.bind = self.__engine
        session = sessionmaker(bind=self.__engine)
        Session = scoped_session(session)
        self.__session = Session

    def close(self):
        """close session"""
        self.__session.close()
