"""
    TokenAuth module
"""
from engine import redis_client as redis
from bson import ObjectId


class TokenAuth:
    """
        Token auth class
    """
    @staticmethod
    def checkToken(token: str):
        """
            Verify the token passed in db is available
            and returns the value present in the db
        """
        tok_key = 'auth_{}'.format(token)

        # get the content of the token
        user_id = redis.get(tok_key)

        if not user_id:
            raise ValueError('User not present')

        # convert user id to objectid and return
        return ObjectId(user_id)
