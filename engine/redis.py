import redis
import keys
from typing import Dict
import json

class RedisClient:
    """
        This class performs all the functions of redis
        needed in the flask app
    """
    def __init__(self) -> None:
        # start connection
        self.__client = redis.Redis(
        host=keys.RED_HOST,
        port=keys.RED_PORT,
        password=keys.RED_PASS
        )


    def set(self, key, value) -> None:
        """
            function to set key and values
            in redis with expiry time
        """
        self.__client.setex(key, 43200, value)

    def get(self, key) -> str:
        """
            function gets a paritcular key
            from redis
        """
        value = self.__client.get(key)
        if not value:
            return None
        return value.decode('utf8')


    def delete(self, key) -> None:
        """
            function deletes a key from
            the redis db
        """
        self.__client.delete(key)

    def addToList(self, list_name: str, content: Dict):
        """
            adds object to a list in redis
        """
        # convert content to string then bytes
        json_str = json.dumps(content)
        json_bytes = json_str.encode('utf-8')

        # store json bytes in redis
        self.__client.rpush(list_name, json_bytes)
        # delete after one hour
        self.__client.expire(list_name, 3600)

    def allList(self, list_name: str):
        """
            returns all the contents of a list in redis
        """
        return self.__client.lrange(list_name, 0, -1)
