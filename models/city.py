#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    if type_storage == 'db':
        state_id = Column(String(128), nullable=False, ForeignKey(state.id))
        name = Column(String(128), nullable=False)
        places = relationship("Place", casade="all, delete", backref="cities")
    else:
        name = ""
        state_id = ""
