#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_type
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete, delete-orphan",
                              backref="state")

    else:
        name = ""

    @property
    def cities(self):
        """rerurn list of cities instance of state_id equal to state.id"""

        from models import storage
        related_city = []
        cities = storage.all(City)
        for city in cities.value():
            if city.state_id == self.id:
                related_city.append(city)
        return related_city
