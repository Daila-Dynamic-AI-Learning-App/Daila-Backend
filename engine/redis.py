import redis

class RedisClient:
    """
        This class performs all the functions of redis
        needed in the flask app
    """
    def __init__(self) -> None:
        # start connection
        self.__client = redis.Redis()


    def set(self, key, value) -> None:
        """
            function to set key and values
            in redis
        """
        self.__client.set(key, value)

    def get(self, key) -> str:
        """
            function gets a paritcular key
            from redis
        """
        return self.__client.get(key).decode('utf8')

    def delete(self, key) -> None:
        """
            function deletes a key from
            the redis db
        """
        self.__client.delete(key)
