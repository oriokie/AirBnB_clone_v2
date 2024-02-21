#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object

time_format = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """A base class for all hbnb models"""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow())
        updated_at = Column(DateTime, default=datetime.utcnow())

        def __init__(self, *args, **kwargs):
            """Instatntiates a new model"""
            if not kwargs:
                from models import storage
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            else:
                update = kwargs['updated_at']
                create = kwargs['created_at']
                if 'updated_at' in kwargs:
                    update = datetime.strptime(update,time_format)
                if 'created_at' in kwargs:
                    create = datetime.strptime(create,time_format)
                if '__class__' in kwargs:
                    del kwargs['__class__']
                else:
                    self.created_at = datetime.now()
                    self.updated_at = self.created_at
                    self.id = str(uuid.uuid4())
                self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
    
    def delete(self):
        """ Function that deletes the current instance from the storage"""
        models.storage.delete(self)