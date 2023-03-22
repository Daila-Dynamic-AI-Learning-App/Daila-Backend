from engine import database, redis_client
from utils.helper import hash_password, generate_uuid
from bcrypt import checkpw
from datetime import datetime
from typing import Dict


class Authorize:
    """
        class to authorize users
    """

    def __init__(self):
        self.__db = database
        self.__redis = redis_client

    def registerUser(self, obj: Dict) -> None:
        """
        takes user's email and password and creates an account
        else raise an error

        Args:
            obj: dictionary containing the user's registration details
        """
        email = obj.get('email')
        password = obj.get('password')

        # check if user with email is present
        if self.__db.findOne('user', {"email": email}):
            raise ValueError(f"User {email} already exists")

        created_at = datetime.now()
        updated_at = datetime.now()

        hashed_password = hash_password(password)
        # add the hashed password to the obj to be stored
        obj['hashed_password'] = hashed_password.decode('utf8')
        obj['created_at'] = created_at
        obj['updated_at'] = updated_at

        # delete the password in the obj
        del obj['password']

        self.__db.addOne('user', obj)

    def loginUser(self, obj: Dict) -> str:
        """
        takes user's email and password and returns the
        user instance associated with it

        Args:
            obj: dictionary containing the user's registration details
        """
        email = obj.get('email')
        password = obj.get('password')

        # get user by email
        user = self.__db.findOne('user', { 'email': email })
        if not user:
            raise ValueError('invalid email')

        # check if password is valid
        if not checkpw(password.encode('utf8'), user.hashed_password.encode('utf8')):
            raise ValueError('incorrect password')

        # generate unique token to store in the redis db
        token = generate_uuid()
        # store user id with token in redis
        self.__redis.set(token, str(user._id))

        return token

AUTH = Authorize()
