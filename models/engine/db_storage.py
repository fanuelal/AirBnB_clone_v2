#!/usr/bin/python3
""" db storage module """

import models
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import City
from models.amenity import Place
from models.amenity import Review
from models.amenity import State
from models.amenity import User
from models.amenity import Amenity


class DBStorage:
    """interacts with the DB"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database storage with environment inputs"""

        dbName = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                dbName
            ),
            pool_pre_ping=True
        )
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a collection of objects"""

        mylist = []
        newdict = {}
        if cls is not None:
            obj = eval(cls)
            mylist = self.__session.query(obj).all()
            for item in mylist:
                key = item.__class__.__name__ + "." + item.id
                newdict[key] = item
        else:
            for obj in ["State", "City", "User",
                        "Place", "Review", "Amenity"]:
                obj = eval(obj)
                mylist = self.__session.query(obj).all()
                for item in mylist:
                    key = item.__class__.__name__ + "." + item.id
                    newdict[key] = item
        return (newdict)

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def new(self, obj):
        """Save a new object to the database"""
        self.__session.add(obj)

    def reload(self):
        """reloads data from the db"""

        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_maker)
        self.__session = Session()

    def save(self):
        """commit all current pending changes to the database"""
        self.__session.commit()
