#!/usr/bin/python3
"""DBStorage class for managing Database interactions"""

import json
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
	"""Class for managing the database interactions"""
	__engine = None
	__session = None

	def __init__(self):
		"""Initializes the database engine"""
		self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
		                              format(os.getenv('HBNB_MYSQL_USER'),
		                                     os.getenv('HBNB_MYSQL_PWD'),
		                                     os.getenv('HBNB_MYSQL_HOST'),
		                                     os.getenv('HBNB_MYSQL_DB'),
		                                     pool_pre_ping=True))
		if os.getenv('HBNB_ENV') == 'test':
			Base.metadata.drop_all(self.__engine)

	def all(self, cls=None):
		"""Method that retrieves a dictionary of all the objects"""

		if cls is None:
			complete_list = []

			for subclass in BaseModel.__subclasses__():
				complete_list.extend(self.__session.query(subclass).all())
				return {"{}.{}".format(type(obj).__name__, obj.id): obj
						for obj in complete_list}
		
		if type(cls) is str:
			cls = eval(cls)
		
		return {"{}.{}".format(type(obj).__name__, obj.id): obj
				for obj in self.__session.query(cls).all()}

	def new(self, obj):
		"""Adds a new object to the current database session"""
		self.__session.add(obj)

	def save(self):
		"""Commits all changes of the current database session"""
		self.__session.commit()

	def delete(self, obj=None):
		"""Deletes an object from the current database session"""
		if obj is not None:
			self.__session.delete(obj)

	def reload(self):
		"""Creates all tables in the database"""
		Base.metadata.create_all(self.__engine)
		session = sessionmaker(bind=self.__engine, expire_on_commit=False)
		Session = scoped_session(session)
		self.__session = Session()

	def close(self):
		"""Closes the current database session"""
		self.__session.close()
