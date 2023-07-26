from engine import database, redis_client
from utils.helper import hash_password, generate_uuid
from bcrypt import checkpw
from models.user import User
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

        hashed_password = hash_password(password)
        # add the hashed password to the obj to be stored
        obj['hashed_password'] = hashed_password.decode('utf8')

        # create user instance
        user = User(**obj)

        self.__db.addOne('user', user.to_dict())

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
        if not checkpw(password.encode('utf8'), user.get("hashed_password").encode('utf8')):
            raise ValueError('incorrect password')

        # generate unique token to store in the redis db
        token = generate_uuid()
        tok_key = 'auth_{}'.format(token)
        # store user id with token in redis
        self.__redis.set(tok_key, str(user.get("_id")))

        return token

    def signOut(self, token: str) -> None:
        """
        takes the token given on login and
        signs the user out
        """
        # get the user id
        tok_key = 'auth_{}'.format(token)
        user_id = self.__redis.get(tok_key)
        if not user_id:
            raise ValueError('User not present')

        # if present, delete token
        self.__redis.delete(tok_key)

AUTH = Authorize()
