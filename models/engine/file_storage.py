#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
"""Imports modules and classes from models file"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

"""Defines a dictionary called classes that maps names to their respective classes"""
classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
         }


class FileStorage:
    """
    This class manages storage of hbnb models in JSON format
    """
    """THe class takes two public attributes. __File_path is the path to which the object will be stored. __object is a dictionary that will hold the objects"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If class name is provided as an argument,
        it returns a dictionary containing only the objects of the class
        """
        dict = {}
        if cls:
            # with .items, use the key and value
            for key, val in self.__objects.items():
                # returns the list of objects of one type of class
                if cls is type(val):
                    # attribute the value to the key
                    dict[key] = val
            return dict
        return self.__objects

    def new(self, obj):
        """
        Adds new object to storage dictionary, ie, __object dictionary.
        The key concatenates the objects name with a dot and objects id.
        """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """
        Saves __object dictionary to json file defines in filepath
        Before saving the objects, __objects are converted to dict
        using to_dict method for each object
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Load __objects dictionary to the json file defined in filepath
        Uses json.loads method to read json file
        and iterates over the dict of loaded objects
        """
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        if  an object is provided as an argument,
        it deletes the object from the __object dictionary
        if no argument is passed it does nothing
        """
        if obj is not None:
            # define the key
            key = obj.__class__.__name__ + '.' + obj.id
            # if there is a key, delete it
            if self.__objects[key]:
                del self.__objects[key]
                self.save()

    def close(self):
        """ close"""
        self.reload()
