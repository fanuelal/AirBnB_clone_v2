#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship

metadata = Base.metadata
Place_amenity = Table('place_amenity', metadata,Column('place_id', String(60), ForeignKey('places.id'),primary_key=True),
                      Column('amenity_id', String(60), ForeignKey('amenities.id')))


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=1)
    number_bathrooms = Column(Integer, nullable=False, default=1)
    max_guest = Column(Integer, nullable=False, default=1)
    price_by_night = Column(Integer, nullable=False, default=1)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship('models.review.Review',
                           backref = 'places',cascade='all, delete')
    amenities = relationship(
        'models.amenity.Amenity',secondary = place_amenity,backref='places', viewonly=False)

    @property
    def reviews(self):
        """getter attribute reviews that returns the list of Review instances"""
        lst = []
        reviews = models.storage.all(models.review.Review)
        for review in reviews.values():
            if review.place_id == self.id:
                lst.append(review)
        return lst

    @property
    def amenities(self):
        """Getter attribute amenities that returns the list of Amenity instances """
        from models.amenity import Amenity
        lst = []
        all_amenities = models.storage.all(Amenity)
        for amenity in all_amenities.values():
            if amenity.place.id == self.id:
                lst.append(amenity)
        return lst

    @amenities.setter
    def amenities(self, value):
        if type(value) == Amenity:
            self.amenity_ids.append(value.id)
