#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import place


class Amenity(BaseModel, Base):
	""" Amenity class """
	if getenv('HBNB_TYPE_STORAGE') == 'db':
		__tablename__ = 'amenities'
		name = Column(String(128), nullable=False)
		place_amenities = relationship(
			"Place", secondary="place_amenity", viewonly=False, back_populates="amenities")

	else:
		name = ""
