from pymongo import MongoClient, ReturnDocument
from typing import Union, Any, Dict
import keys

class Db:
    def __init__(self) -> None:
        self.__client = MongoClient(f"mongodb+srv://{keys.DB_USER}:{keys.DB_SECRET}@cluster0.pho2egn.mongodb.net/?retryWrites=true&w=majority")
        self.__db = self.__client[keys.DB_NAME]

    def addOne(self, collection: str, obj: Dict):
        """
            adds a collection with obj to the database
        """
        field = self.__db[collection]
        field.insert_one(obj)

    def findOne(self, collection: str, obj: Dict) -> Union[Any, None]:
        """
            find one obj in collection in the database
        """
        field = self.__db[collection]
        return field.find_one(obj)

    def findAll(self, collection: str, obj: Dict) -> Union[Any, None]:
        """
            find all obj that matches in collection in the database
        """
        field = self.__db[collection]
        return field.find(obj)

    def deleteOne(self, collection: str, obj: Dict) -> None:
        """
            deletes a collection from the database
        """
        field = self.__db[collection]
        field.delete_one(obj)

    def findUpdateOne(self, collection, obj: Dict, update: Dict):
        """
            find and updates a collection in the database
        """
        field = self.__db[collection]
        return field.find_one_and_update(obj, update, return_document=ReturnDocument.AFTER)


# data_b = Db()
# elem = data_b.addOne('user', { 'name': 'foo', 'email': 'goo@g.com' })
# print(dir(elem))
