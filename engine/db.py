from pymongo import MongoClient
from typing import Union, Any, Dict


class Db:
    def __init__(self) -> None:
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client['test']

    def addOne(self, collection: str, obj: Dict) -> None:
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

    def deleteOne(self, collection: str, obj: Dict) -> None:
        """
            deletes a collection from the database
        """
        field = self.__db[collection]
        field.delete_one(obj)

# data_b = Db()
# elem = data_b.addOne('user', { 'name': 'foo', 'email': 'goo@g.com' })
# print(dir(elem))
