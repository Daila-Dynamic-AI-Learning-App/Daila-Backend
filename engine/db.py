from pymongo import MongoClient


class Db:
    def __init__(self) -> None:
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client['test']

    def addOne(self, collection, obj):
        """
            adds a collection with obj to the database
        """
        field = self.__db[collection]
        field.insert_one(obj)

    def findOne(self, collection, obj):
        """
            find one obj in collection in the database
        """
        field = self.__db[collection]
        return field.find_one(obj)

    def deleteOne(self, collection, obj):
        """
            deletes a collection from the database
        """
        field = self.__db[collection]
        field.delete_one(obj)

# data_b = Db()
# elem = data_b.addOne('user', { 'name': 'foo', 'email': 'goo@g.com' })
# print(dir(elem))
