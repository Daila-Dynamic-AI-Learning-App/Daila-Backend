import redis
import keys

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
